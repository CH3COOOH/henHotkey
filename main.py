# -*- coding: utf-8 -*-
import keyboard
import pyperclip
import time
import sys
import json
import multiprocessing

MODIFIERS = set(['ctrl', 'alt', 'shift', 'win'])
SELF_TEST_TIMEOUT = 10
CHECK_INTERVAL = 10

class HotkeyController:
	def __init__(self, _id=int(time.time())):
		self.id = _id
		self.last_self_test_ok_ts = 0
		self.templates = None
	
	def clear_hotkeys(self):
		keyboard.clear_all_hotkeys()
		print(f"[{self.id}]_clear_hotkeys()")

	def _self_test_callback(self):
		self.last_self_test_ok_ts = time.time()
		print(f"[{self.id}]_self_test_cb(): t={self.last_self_test_ok_ts}")

	def _hotkey_split(self, hk):
		return set(hk.split('+'))

	def watchdog_loop(self):
		while True:
			now = time.time()
			if now - self.last_self_test_ok_ts > SELF_TEST_TIMEOUT:
				print(f"[{self.id}]watchdog_loop(): Hook timeout. Restarting daemon...")
				self.clear_hotkeys()
				break
			time.sleep(CHECK_INTERVAL)

	def release_keys(self, keys):
		for k in keys:
			try: keyboard.release(k)
			except: pass

	def block_keys(self, keys):
		for k in keys:
			try: keyboard.block_key(k)
			except: pass

	def unblock_keys(self, keys):
		for k in keys:
			try: keyboard.unblock_key(k)
			except: pass

	def paste_text(self, hk, text: str, use_shift_insert=False):
		in_keys = self._hotkey_split(hk)
		in_keys_xmod = in_keys - MODIFIERS
		ope_keys = None
		self.block_keys(in_keys_xmod)
		self.release_keys(in_keys)
		self._self_test_callback()
		print(f"[{self.id}]paste_text(): {hk} -> {text[0]}***")
		pyperclip.copy(text)
		time.sleep(0.1)  # <- Wait for copying to clipboard
		if use_shift_insert:
			keyboard.press_and_release('shift+insert')
			ope_keys = set(['shift', 'insert'])
		else:
			keyboard.press_and_release('ctrl+v')
			ope_keys = set(['ctrl', 'v'])
		time.sleep(0.05)  # <- Wait for recognizing hotkey
		self.release_keys(ope_keys)
		self.unblock_keys(in_keys_xmod)

	def register_hotkeys(self):
		for hk, txt in self.templates.items():
			keyboard.add_hotkey(hk, lambda t=txt, h=hk: self.paste_text(h, t), suppress=False)
		self.last_self_test_ok_ts = time.time()
	
	def load_templates(self, fname):
		with open(fname, 'r', encoding='utf-8') as o:
			self.templates = json.load(o)

def start_an_instance():
	hc = HotkeyController()
	hc.load_templates(sys.argv[1])
	print('start_an_instance(): Register hotkeys...')
	hc.register_hotkeys()
	hc.watchdog_loop()
	return -1

def main():
	while True:
		p = multiprocessing.Process(target=start_an_instance)
		p.start()
		p.join()
		time.sleep(.5)

if __name__ == '__main__':
	main()