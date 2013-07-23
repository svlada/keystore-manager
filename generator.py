import ConfigParser
import subprocess
import os
import sys

class KeyStoreManager:

	def __init__(self, config):
		self.config = config

	def generate_private_key(self):
		""" Generate Private Key  """
		cmd = ('genrsa -des3 -out private.pem 2048')
		process = subprocess.Popen(['openssl'], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
		print process.communicate(cmd)[0]

	def generate_certificate(self):
		cmd = ('openssl req -new -x509 -key private.pem -out public.crt')
		process_keytool = subprocess.Popen(cmd, shell=True)
		process_keytool.communicate()

	def merge_private_and_cert_to_pkcs12(self, alias):
		print "merge_private_public_to_pkcs12"

		cmd = (
			'pkcs12 -export' + 
			' -in public.crt' +
			' -inkey private.pem' + 
			' -out temp.pkcs12' + 
			' -name ' + alias
		)

		process = subprocess.Popen(['openssl'], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
		print process.communicate(cmd)[0]

	def import_private_and_cert_to_jks(self, alias):

		cmd = (
			'keytool -importkeystore ' +  
			'-deststorepass secret ' +
			'-destkeypass  secret ' +
			'-destkeystore keystore.jks ' +
			'-srckeystore temp.pkcs12 -srcstoretype PKCS12 ' +
			'-srcstorepass secret ' +
			'-alias '+ alias
		)
		process_keytool = subprocess.Popen(cmd, shell=True)
		process_keytool.communicate()

config = {}

keyStoreManager = KeyStoreManager(config)
keyStoreManager.generate_private_key()
keyStoreManager.generate_certificate()
keyStoreManager.merge_private_and_cert_to_pkcs12("idp")
keyStoreManager.import_private_and_cert_to_jks("idp")