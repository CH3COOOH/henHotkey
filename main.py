# -*- coding: utf-8 -*-
import keyboard
import pyperclip
import time
import sys
import json
import multiprocessing

MODIFIERS = ('ctrl', 'alt', 'shift', 'win')
SELF_TEST_HK = 'f23+f24'
SELF_TEST_TIMEOUT = 13
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

	def _alive_probe(self):
		try:
			keyboard.press_and_release(SELF_TEST_HK)
			# keyboard.send(SELF_TEST_HK)
			self.release_modifiers()
			print(f"[{self.id}]_alive_probe(): Press {SELF_TEST_HK}")
		except Exception:
			print(f"[{self.id}]_alive_probe(): X")
			pass

	def watchdog_loop(self):
		while True:
			now = time.time()
			multiprocessing.Process(target=self._alive_probe, daemon=True).start()
			if now - self.last_self_test_ok_ts > SELF_TEST_TIMEOUT:
				print(f"[{self.id}]watchdog_loop(): Hook dead. Restarting daemon...")
				self.clear_hotkeys()
				break
			time.sleep(CHECK_INTERVAL)

	def release_modifiers(self):
		for mod in MODIFIERS:
			try: keyboard.release(mod)
			except: pass

	def paste_text(self, text: str, use_shift_insert=False):
		self.release_modifiers()
		print(f"[{self.id}]paste_text(): " + text[0] + '***')
		pyperclip.copy(text)
		time.sleep(0.05)
		if use_shift_insert:
			keyboard.press_and_release('shift+insert')
		else:
			keyboard.press_and_release('ctrl+v')
		time.sleep(0.05)
		self.release_modifiers()

	def register_hotkeys(self):
		for hk, txt in self.templates.items():
			keyboard.add_hotkey(hk, lambda t=txt: self.paste_text(t), suppress=False)
		keyboard.add_hotkey(SELF_TEST_HK, self._self_test_callback, suppress=False)
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