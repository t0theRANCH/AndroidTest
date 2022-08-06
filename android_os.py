import json
from jnius import autoclass, cast

# Some random Android functions to use for Kivy in Python


class CipherTextWrapper:
    def __init__(self, cipher, iv):
        self.cipher = ','.join([str(x) for x in cipher])
        self.iv = ','.join([str(x) for x in iv])


class Android:
    def __init__(self, app_name):
        self.app_name = app_name
        self.PythonActivity = self.get_activity()
        self.currentActivity = self.get_current_activity()
        self.context = self.get_context()
        self.prefs = self.get_shared_prefs()

    @staticmethod
    def get_activity():
        return autoclass('org.kivy.android.PythonActivity')

    def get_key(self, prefs):
        KeyStore = autoclass('java.security.KeyStore')
        keyStore = KeyStore.getInstance("AndroidKeyStore")
        keyStore.load(None)
        key = keyStore.getKey(self.app_name, None)
        if key:
            cipherTextWrapper = json.loads(prefs.getString('password', None))
        else:
            cipherTextWrapper = None
        return key, cipherTextWrapper

    @staticmethod
    def get_cipher():
        Cipher = autoclass('javax.crypto.Cipher')
        return Cipher.getInstance("AES/GCM/NoPadding")

    def encrypt_key(self, password):
        KeyProperties = autoclass('android.security.keystore.KeyProperties')
        KeyGenerator = autoclass('javax.crypto.KeyGenerator')
        KeyGenParameterSpec = autoclass('android.security.keystore.KeyGenParameterSpec$Builder')

        kg = KeyGenParameterSpec(self.app_name, KeyProperties.PURPOSE_ENCRYPT | KeyProperties.PURPOSE_DECRYPT)
        kg.setBlockModes(KeyProperties.BLOCK_MODE_GCM)
        kg.setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
        keyGenerator = KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore")
        keyGenerator.init(kg.build())

        cipher = Android.get_cipher()
        cipher.init(1, cast('java.security.Key', keyGenerator.generateKey()))
        return [cipher.doFinal(cast('java.lang.String', password).getBytes("UTF-8")), cipher.getIV()]

    def decrypt_key(self):
        GCMParameterSpec = autoclass('javax.crypto.spec.GCMParameterSpec')
        String = autoclass('java.lang.String')

        secretKey, cipherTextWrapper = self.get_key(self.prefs)
        cipher = self.get_cipher()

        iv = [int(x) for x in cipherTextWrapper['iv'].split(",")]
        e = [int(x) for x in cipherTextWrapper['cipher'].split(",")]

        cipher.init(2, secretKey, GCMParameterSpec(128, iv))
        decryptedData = cipher.doFinal(e)
        p = String(decryptedData, "UTF-8").toCharArray()
        return ''.join(p)

    def get_current_activity(self):
        return cast('android.app.Activity', self.PythonActivity.mActivity)

    def get_context(self):
        return cast('android.content.Context', self.currentActivity.getApplicationContext())

    def get_shared_prefs(self):
        return self.context.getSharedPreferences(self.app_name, self.context.MODE_PRIVATE)

    def add_shared_prefs(self, key, value):
        editor = self.prefs.edit()
        editor.putString(key, value)
        editor.commit()

    def add_password_shared_prefs(self, cipher, iv):
        editor = self.prefs.edit()
        j = json.dumps(CipherTextWrapper(cipher, iv).__dict__)
        editor.putString('password', j)
        editor.commit()

    def get_prefs_entry(self, key):
        return self.prefs.getString(key, None)
