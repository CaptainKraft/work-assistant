#!/usr/bin/env -S python3 -u
# -*- coding: UTF-8 -*-
import os                          # os.path.join, os.getcwd, os.chdir, os.listdir, os.rename, os.makedirs, os.path.isdir, os.rmdir, os.remove, os.path.isfile, os.path.islink, os.path.dirname, os.readlink, os.path.abspath, os.cpu_count, os.replace, os.path.basename
import io                          # io.TextWrapper
import sys                         # sys.path, sys.argv, sys.exit
import json                        # json.load, json.JSONDecodeError, json.dump
import pickle                      # pickle.load, pickle.PickleError, pickle.dump
import re                          # re.match, re.sub
import functools                   # functools.cmp_to_key
import shutil                      # shutil.move, shutil.copy, shutil.unpack_archive, shutil.which
import shlex                       # shlex.split
import subprocess                  # subprocess.Popen, subprocess.PIPE, subprocess.STDOUT
import time	                       # time.time
import platform                    # platform.system
import urllib.request              # urllib.request.urlopen
import urllib.error                # urllib.error.HTTPError, urllib.error.URLError
import typing                      # typing.TypeVar, typing.TypeAlias
import threading                   # threading.Lock
import tempfile                    # for atomic deletion
import signal                      # signal.strsignal
import xml.etree.ElementTree as ET # for xml writing
from   xml.dom import minidom      # for xml pretty print
import concurrent.futures
import stat
import traceback
from datetime import datetime
from contextlib import contextmanager
from types import TracebackType
from typing import Type, Callable, Generator, Union, Optional, List, Dict, Set, Any

LLVM_VERSION = '20.1.7'
CMAKE_VERSION = '3.30.4'

# Work out TypeAlias which is a Python 3.10.x feature
if sys.version_info >= (3, 10):
	from typing import TypeAlias
else:
	def TypeAlias(self, parameters):
		pass
# Work out Self which is a Python 3.11.x feature
if sys.version_info >= (3, 11):
	from typing import Self
else:
	def Self(self, params):
		pass

# We prefer all types are CamelCase, even builtin ones. We prefer the use of
# TypeAlias and TypeVar over the more recent Python 3.10.x 'type' statements
# here in comments since macOS Python ships with Python 3.9.x. This should be
# changed in the future.
String: TypeAlias = str
Bool:   TypeAlias = bool
Int:    TypeAlias = int
Map:    TypeAlias = Dict

class Sublime:
	name: String
	path: String
	file: Dict[String, Any]
	def __init__(self: Self, name: String, path: String):
		self.name = name
		self.path = path
		self.file = {
			'folders': [
				{
					'name': name,
					'path': '.',
					'folder_exclude_patterns': [
						'.*',
						'*/images',
						'experiments',
						'tools',
						'tests',
						'build',
						'Odin/bin',
						'Odin/ci',
						'Odin/shared',
						'Odin/examples',
						'Odin/misc',
						'Odin/src',
					],
					'file_exclude_patterns': [
						'.*',
						'*.dll',
						'*.exe',
						'*.pdb',
						'*.dat',
						'*.il',
						'*.o',
						'*.d',
						'Odin/**'
					]
				},
			],
			'build_systems': [
				{
					'name': name,
					'file_regex': '^\\s*((?:.+?)[\\/\\\\](?:[^\\/\\\\]+?))\\((\\d+)\\:(\\d+)\\)[\\s\\w]+\\:\\s(.+)$',
					'env': {
						'JFX_BUILD_QUIET': '1',
						'JFX_BUILD_COLOR': '0',
					},
					'shell_cmd': f'python -u ${{project_path}}/build/main.py build quick {self.name}',
					'quiet': True,
					'selector': 'source.odin',
					'working_dir': f'${{project_path:${{folder}}}}/{path}',
					'variants': []
				}
			]
		}
	def add_config(self: Self, name: String, action: String, config: String):
		self.file['build_systems'][0]['variants'].append({
			'shell_cmd': f'python -u ${{project_path}}/build/main.py {action} {config} {self.name}',
			'name': name,
		})
	def add_folder_exclude(self: Self, excl: String):
		self.file['folders'][0]['folder_exclude_patterns'].append(excl)
	def save(self: Self, output_dir: String):
		with open(os.path.join(output_dir, f'{self.name}.sublime-project'), 'w') as fp:
			fp.write(json.dumps(self.file, indent = 2))

class VSCode:
	name: String
	path: String
	file: Dict[String, Any]
	def __init__(self: Self, name: String, path: String):
		self.name = name
		self.path = path
		self.file = {
			'folders': [
				{
					'name': name,
					'path': '.',
				},
			],
			'settings': {
				'files.exclude': {
					'**/.*': True,
					'**/images/**': True,
					'experiments/**': True,
					'tools/**': True,
					'tests/**': True,
					'build/**': True,
					'Odin/bin/**': True,
					'Odin/ci/**': True,
					'Odin/shared/**': True,
					'Odin/examples/**': True,
					'Odin/misc/**': True,
					'Odin/src/**': True,
					'**/*.dll': True,
					'**/*.exe': True,
					'**/*.pdb': True,
					'**/*.dat': True,
					'**/*.il': True,
					'**/*.o': True,
					'**/*.d': True,
				},
			},
			'tasks': {
				'version': '2.0.0',
				'options': {
					'env': {
						'JFX_BUILD_QUIET': '1',
					},
					'cwd': f'${{workspaceFolder:{self.name}}}/{self.path}'
				},
				'tasks': [
				],
			}
		}
	def add_config(self: Self, name: String, action: String, config: String):
		task = {
			'label': name,
			'command': 'python',
			'type': 'shell',
			'args': [
				f'${{workspaceFolder:{self.name}}}/build/main.py',
				action,
				config,
				self.name
			],
			'presentation': {
				'reveal': 'silent'
			},
			'group': 'build'
		}
		self.file['tasks']['tasks'].append(task)
	def add_folder_exclude(self: Self, excl: String):
		self.file['settings']['files.exclude'][excl] = True
	def save(self: Self, output_dir: String):
		with open(os.path.join(output_dir, f'{self.name}.code-workspace'), 'w') as fp:
			fp.write(json.dumps(self.file, indent = 2))

def lstree(path: String, topdown: Bool = False) -> Generator[String, None, None]:
	def error(ex):
		raise ex
	for root, dirs, files in os.walk(path, topdown, followlinks=False, onerror=error):
		for file in files:
			yield os.path.join(root, file)
		for dir in dirs:
			yield os.path.join(root, dir)

def lstrees(paths: List[String], topdown: Bool = False):
	for path in paths:
		for item in lstree(path, topdown):
			yield item

# Less error-prone chdir. Will restore the original directory always, even in
# the face of exceptions.
@contextmanager
def pushd(path: String):
	old = os.getcwd()
	os.chdir(path)
	try:
		yield
	finally:
		os.chdir(old)

class Progress:
	SIZE = 30
	message: String
	def __init__(self: Self, quiet: Bool):
		self.start = time.time()
		self.message = ""
		self.quiet = quiet
	def reset(self: Self, message: String):
		if not self.quiet and self.message != "":
			self.done('✓')
		self.start = time.time()
		self.message = message
		if self.quiet:
			print(f'{message} ...')
		else:
			print(f'{message} ...', end='\r', file=sys.stdout, flush=True)
	def label(self: Self) -> String:
		# +1 for ' ' +1 for '[' and +1 for ']'
		n = 42 - (len(self.message) + 3)
		return f'{self.message}{" "*n}'
	def show(self: Self, count: Int, j: Int):
		if self.quiet:
			return
		along = int(self.SIZE * j / max(count, 1))
		remain = ((time.time() - self.start) / max(j, 1)) * (count - j)
		mins, sec = divmod(remain, 60)
		eta = f'{int(mins):02}:{sec:03.1f}'
		print(f'{self.label()} [{u"█"*along}{("."*(self.SIZE - along))}] {j}/{count} ETA {eta}', end='\r', file=sys.stdout, flush=True)
	def done(self: Self, msg: String):
		if self.message == "" or self.quiet:
			return
		# Ensure the entire line is erased since it might be longer than the DONE
		# line
		dt = time.time() - self.start
		print('\033[K', end='\r', file=sys.stdout, flush=True)
		print(f'{self.label()} [{u"█"*self.SIZE}] {msg} {dt:.6f}s', end='\r', file=sys.stdout, flush=True)
		print('', file=sys.stdout, flush=True)
	def skip(self: Self):
		if self.quiet:
			return
		print('\033[K', end='\r', file=sys.stdout, flush=True)
		print(f'{self.label()} [{u"█"*self.SIZE}] Skipped', end='\r', file=sys.stdout, flush=True)
		print('', file=sys.stdout, flush=True)

class Error(Exception):
	pass

# Most targets are represented by a package. Multiple packages for a target with
# different versions are called a Bundle. This class representes such a bundle.
class Bundle:
	name:     String
	pkgs:     List[String]
	versions: List[String] # The detected package version
	selected: Int          # The selected package version (index into versions)

	def key(self: Self) -> String:
		return f'{self.name}-{self.versions[self.selected]}'

	def src_path(self: Self) -> String:
		return os.path.join('.src', self.key())

	# Regular expression to match valid package files. Contains a capture group
	# for the version in \1 and the extension in \2.
	def pkg_re(self: Self):
		return rf'{self.name}-([\d.]+)\.(zip|tar\.gz)$'
	# Get the list of all packages which match pkg_re
	def pkg_list(self: Self) -> List[String]:
		return list(filter(lambda item: re.match(self.pkg_re(), item), os.listdir('pkg')))
	def pkg_path(self: Self) -> String:
		return os.path.join('pkg', self.pkgs[self.selected])

	def __init__(self: Self, name: String, urls: List[Map[String, String]]):
		self.name = name
		self.pkgs = self.pkg_list()
		if len(self.pkgs) == 0 and len(urls) != 0:
			print(f'Could not find package: "{name}"')
			# Some packages we download instead of storing in the repository because
			# they are too large. The download takes place here.
			for url in urls:
				src = url.get('src', None)
				dst = url.get('dst', None)
				if not src: raise Error(f'Could not find "src": "{url}"')
				if not dst: raise Error(f'Could not find "dst": "{url}"')
				print(f'  Downloading: "{src}" ...')
				try:
					with urllib.request.urlopen(src, timeout=30) as response:
						file = os.path.join('pkg', f'{dst}.COPYME')
						with open(file, 'wb') as fp:
							fp.write(response.read())
						# We atomically rename it here when done so we don't end up with a
						# partial or incomplete download that is treated as completed.
						os.rename(file, os.path.join('pkg', dst))
					self.pkgs.append(dst)
					break
				except (urllib.error.HTTPError, urllib.error.URLError) as error:
					print(f'    Error: {error.reason}')
					continue
		# There should be a {name}-{version}.(zip|tar.gz) in the paths list here otherwise
		# the target cannot be built. We permit multiple versions of the package in
		# the pkg directory but we always pick the latest one using a version sort.
		if len(self.pkgs) == 0:
			raise Error(f'Could not find package: "{name}"\n'
			            f'  No files matching "pkg/{name}-{{version}}.(zip|tar.gz)" found')
		versions = [re.sub(self.pkg_re(), r'\1', path) for path in self.pkgs]
		def cmp(lhs: Int, rhs: Int) -> Int:
			version = lambda x: tuple(map(int, (x.split('.'))))
			lhsrank = version(versions[lhs])
			rhsrank = version(versions[rhs])
			if   lhsrank > rhsrank: return -1
			elif lhsrank < rhsrank: return  1
			return 0
		self.versions = versions
		self.selected = sorted(range(len(versions)),
		                       key=functools.cmp_to_key(cmp))[0]

class Project:
	name: String
	path: String
	def __init__(self: Self, name: String, path: String):
		self.name = name
		self.path = path
	def key(self: Self) -> String:
		return self.name
	def src_path(self: Self) -> String:
		return self.path

class Target:
	name: String
	deps: List[String]
	ignr: List[String]
	kind: Union[Bundle, Project]

	def __init__(self: Self,
	             name: String,
	             deps: List[String],
	             ignr: List[String],
	             date: Bool,
	             kind: Union[Bundle, Project]):
		self.name = name
		self.deps = deps
		self.ignr = ignr
		self.date = date
		self.kind = kind

	# Regardless of what 'config' is always select 'release' unless overrided.
	def config(self: Self, config: String) -> String:
		return 'release'

	def ignored(self: Self, file: String) -> Bool:
		# We do not care to check Ninja build logs but we still track them.
		if re.match(r'^.*\.ninja_log$', file):
			return True
		for ignr in self.ignr:
			if re.match(ignr, file):
				return True
		return False

	def key(self: Self) -> String:
		return self.kind.key()

	def src_path(self: Self) -> String:
		return self.kind.src_path()
	def tmp_path(self: Self) -> String:
		return os.path.join('.tmp', self.key())

	def configure(self: Self, config: String, build: 'Build'):
		build.cmake_configure(config)
	def compile(self: Self, config: String, build: 'Build'):
		build.cmake_compile(config)
	def install(self: Self, config: String, build: 'Build'):
		build.cmake_install(config)

class Toolchain:
	cc:       String
	cxx:      String
	ar:       String
	mt:       String
	objcopy:  String

	# Find a Windows Kit for mt.exe
	def findmt(self: Self) -> String:
		KIT  = '10'
		kits = os.path.join(os.environ['ProgramFiles(x86)'], 'Windows Kits', KIT, 'bin')
		for path in os.listdir(kits):
			if path.startswith(KIT):
				mtpath = os.path.join(kits, path, 'x64', 'mt.exe')
				if os.path.exists(mtpath):
					return mtpath
		raise Error(f'Could not find MT.exe')

	# Helper to get the name of a library, since this is platform specific:
	# Unix:    lib{name}.a
	# Windows: {name}.lib
	def libname(self: Self, name: String) -> String:
		if platform.system() == 'Windows':
			return f'{name}.lib'
		else:
			return f'lib{name}.a'

	def __init__(self: Self, prefix: String):
		path = os.path.join(prefix, 'bin')
		if platform.system() == 'Windows':
			self.cc = os.path.join(path, 'clang-cl.exe')
			self.cxx = os.path.join(path, 'clang-cl.exe')
			self.ar = os.path.join(path, 'llvm-ar.exe')
			self.objcopy = os.path.join(path, 'llvm-objcopy.exe')
			self.mt = self.findmt()
		else:
			self.cc = os.path.join(path, 'clang')
			self.cxx = os.path.join(path, 'clang++')
			self.ar = os.path.join(path, 'llvm-ar')
			self.objcopy = os.path.join(path, 'llvm-objcopy')
			self.mt = ""

# When generating the plist for macOS bundle we use this to generate the plist
class PList:
	class Element:
		def __init__(self: Self, plist: 'PList', element: ET.Element):
			self.plist = plist
			self.element = element
		def subelement(self: Self, key: String) -> 'PList.Element':
			return PList.Element(self.plist, ET.SubElement(self.element, key))
		def write(self: Self, key: Optional[String], value: Optional[Union[Bool, String, List[String]]]):
			if key:
				ET.SubElement(self.element, 'key').text = key
			if value != None:
				if isinstance(value, Bool):
					ET.SubElement(self.element, 'true' if value else 'false')
				elif isinstance(value, String):
					ET.SubElement(self.element, 'string').text = value
				elif isinstance(value, list):
					array = self.subelement('array')
					for v in value:
						array.write(None, v)
				else:
					raise TypeError('Unsupported type')
	def __init__(self: Self):
		self.element = ET.Element('plist')
		self.element.set('version', '1.0')
	def subelement(self: Self, key: String) -> Element:
		return PList.Element(self, ET.SubElement(self.element, key))
	def render(self: Self) -> String:
		XML = f'''
			<?xml version="1.0" encoding="UTF-8"?>
			<!DOCTYPE plist
				PUBLIC "-//Apple//DTD PLIST 1.0//EN"
				"http://www.apple.com/DTDs/PropertyList-1.0.dtd">
			{ET.tostring(self.element, xml_declaration=False).decode()}
		'''.strip()
		return minidom.parseString(XML).toprettyxml(indent="  ")

class Build:
	root:      String
	configs:   List[Map[String, Any]]
	prefix:    String
	environ:   List[Callable[[], Map[String, String]]]
	targets:   Map[String, Target]
	progress:  Progress
	writable:  Set[String]
	toolchain: Toolchain

	# Returns true for configs that produce builds for dev users
	@staticmethod
	def is_dev(config: String) -> Bool:
		return config != 'shipping' and config != 'internal'

	# Simple stack based management of the environment.
	class Env:
		def __init__(self: Self, build: 'Build', environ: Map[String, String]):
			self.build = build
			self.environ = environ
		def __enter__(self: Self) -> Self:
			def ENV() -> Map[String, String]:
				return self.environ
			self.build.environ.append(ENV)
			return self
		def __exit__(self: Self,
		             type:      Optional[Type[BaseException]],
		             value:     Optional[BaseException],
		             traceback: Optional[TracebackType]) -> Optional[Bool]:
			self.build.environ.pop()
			return None

	def config(self: Self, name: String, default = None) -> Any:
		return self.configs[-1].get(name, default)

	def env(self: Self, environ: Map[String, String]) -> Env:
		return Build.Env(self, environ)

	def mv(self: Self, src: String, dst: String):
		shutil.move(src, dst)
		os.utime(dst, None)
		self.writable.discard(src)
		# self.log(f'[+] Moved file "{src}" -> "{dst}"')

	def cp(self: Self, src: String, dst: String):
		shutil.copy(src, dst)
		# self.log(f'[+] Copied file "{src}" -> "{dst}"')

	def chmod(self: Self, root: String):
		items = root.split(os.path.sep)
		for i, item in enumerate(items):
			path = os.path.sep.join(items[:i+1])
			# When we've already seen this writable path we can skip it.
			if path not in self.writable:
				try:
					os.chmod(path, stat.S_IRWXU)
					self.writable.add(path)
				except:
					pass

	def rm(self: Self, path: String) -> Bool:
		removed = False
		try:
			# We just unlink symlinks directly since this is already atomic.
			if os.path.islink(path):
				os.unlink(path)
				return True
			# Ensure we have write permissions to rename the file.
			self.chmod(path)
			# Rename to temporary directory for atomicity
			with tempfile.TemporaryDirectory() as tmp:
				delete = os.path.join(tmp, os.path.basename(path))
				shutil.move(path, delete)
				self.writable.discard(delete)
				removed = True
			# self.log(f'[+] Removed file "{path}"')
		except FileNotFoundError:
			# Not an error to remove an already removed file.
			pass
		return removed

	# This recursively removes everything just to be more robust.
	def rmdir(self: Self, path: String) -> Bool:
		removed = False
		try:
			# Ensure we have write permissions to rename the directory.
			self.chmod(path)
			with tempfile.TemporaryDirectory() as tmp:
				delete = os.path.join(tmp, os.path.basename(path))
				shutil.move(path, delete)
				self.writable.discard(delete)
				removed = True
			# self.log(f'[+] Removed directory "{path}"')
		except FileNotFoundError:
			# Not an error to remove an already removed directory.
			pass
		return removed

	def mkdir(self: Self, path: String):
		try:
			os.makedirs(path)
			# self.log(f'[+] Created directory "{path}"')
		except FileExistsError:
			# Not an error to make a directory that already exists.
			pass

	def rmseq(self: Self, items: List[String], progress: Optional[Callable[[Int, Int], None]] = None) -> Bool:
		for i, item in enumerate(items):
			if os.path.isdir(item):
				self.rmdir(item)
			else:
				self.rm(item)
			if progress:
				progress(i, len(items))
		return len(items) != 0

	def rmtree(self: Self, path: String) -> Bool:
		if self.rmdir(path):
			self.log(f'[+] Removed tree "{path}"')
			return True
		return False

	def optree(self: Self, src: String, dst: String, op: Callable[[String, String], None], progress: Optional[Callable[[Int, Int], None]] = None) -> Bool:
		self.mkdir(dst)
		items = list(lstree(src, True))
		links = []
		files = []

		# On the first pass we're going to create the directory structure and keep
		# track of files and links. This part has to be done in-order.
		for i, item in enumerate(items):
			joined = os.path.join(dst, os.path.relpath(item, src))
			if os.path.islink(item):
				links.append(item)
			elif os.path.isdir(item):
				self.mkdir(joined)
			else:
				files.append((item, joined))
			if progress:
				progress(i, len(items))

		# On the second pass we can perform the op out of order which we will using
		# multiple threads since this is also where the rubber meets the road.
		futures = []
		threads = int(self.config('jobs'))
		with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as exec:
			def wrap(items):
				try:
					for item in items:
						op(item[0], item[1])
				except KeyboardInterrupt:
					pass
			files_per_batch = (len(files) + threads - 1) // threads
			batches = [files[i:i+files_per_batch] for i in range(0, len(files), max(1, files_per_batch))]
			for batch in batches:
				futures.append(exec.submit(wrap, batch))

		# We can then wait for each one as they complete.
		i = 0
		for future in concurrent.futures.as_completed(futures):
			if progress:
				progress(i, len(items))
			i += 1

		# The links have to be done last once all files are copied or moved. This
		# could also be spread over many threads but since we expect there to be few
		# links it's likely not worth it.
		for i, link in enumerate(links):
			joined = os.path.join(dst, os.path.relpath(link, src))
			target = os.readlink(link)
			if os.path.isabs(target):
				target = os.path.relpath(target, os.path.dirname(link))
			os.symlink(target, joined, os.path.isdir(link))
			# self.log(f'[+] Created link "{joined} -> "{target}"')
			if progress:
				progress((len(items) - len(links)) + i, len(items))
		return len(items) != 0

	def cptree(self: Self, src: String, dst: String, progress: Optional[Callable[[Int, Int], None]] = None):
		def _op(src: String, dst: String):
			if os.path.isdir(src):
				self.mkdir(dst)
			else:
				self.cp(src, dst)
		if self.optree(src, dst, _op, progress):
			self.log(f'[+] Copied tree "{src}" -> "{dst}"')

	def mvtree(self: Self, src: String, dst: String, progress: Optional[Callable[[Int, Int], None]] = None):
		def _op(src: String, dst: String):
			self.mv(src, dst)
		op_status = self.optree(src, dst, _op, progress)
		rm_status = self.rmtree(src)
		if op_status or rm_status:
			self.log(f'[+] Moved tree "{src}" -> "{dst}"')

	def log(self: Self, message: String):
		encoded = message.encode()
		newline = '\n'.encode()
		with self.loglock:
			self.logfile.write(encoded)
			self.logfile.write(newline)
			self.logfile.flush()

	# CMake helpers
	def cmake_configure(self: Self, config: String, opts: List[String] = []):
		# So long as we have a compiled LLVM we can use it as our C and C++ compiler
		toolchain = []
		if platform.system() == 'Windows':
			# We static link everything (i.e want /MT, not /MD)
			toolchain.append('-DCMAKE_POLICY_DEFAULT_CMP0091=NEW')
			toolchain.append('-DCMAKE_MSVC_RUNTIME_LIBRARY=MultiThreaded')
		if self.checkpoint(self.targets['llvm'], 'install')['reached']:
			if platform.system() == 'Windows':
				toolchain.append(f'-DCMAKE_MT={self.toolchain.mt}')
			toolchain.extend([
				f'-DCMAKE_C_COMPILER={self.toolchain.cc}',
				f'-DCMAKE_CXX_COMPILER={self.toolchain.cxx}',
				f'-DCMAKE_C_ARCHIVE={self.toolchain.ar}',
				f'-DCMAKE_CXX_ARCHIVE={self.toolchain.ar}',
				f'-DCMAKE_C_ARCHIVE={self.toolchain.ar}'
			])
		self.run([
			'cmake',
			'-Wno-dev',
			'-B', '.build-{}'.format(config),
			'-G', 'Ninja',
			'-DBUILD_SHARED_LIBS=OFF',
			'-DBUILD_STATIC_LIBS=ON',
			'-DCMAKE_BUILD_TYPE={}'.format('Release' if config == 'release' else 'Debug'),
			'-DCMAKE_WARN_DEPRECATED=OFF',
			'-DCMAKE_INSTALL_PREFIX={}'.format(self.prefix),
			'-DCMAKE_PREFIX_PATH={}'.format(self.prefix),
			'-DCMAKE_SYSTEM_INCLUDE_PATH={}'.format(os.path.join(self.prefix, 'include')),
			'-DCMAKE_INSTALL_LIBDIR=lib',
			'-DCMAKE_POSITION_INDEPENDENT_CODE=ON',
			*toolchain
		] + opts)
	def cmake_compile(self: Self, config: String, opts: List[String] = []):
		self.run([ 'cmake', '--build', f'.build-{config}', '--parallel', str(self.config('jobs')), '--verbose' ] + opts)
	def cmake_install(self: Self, config: String, opts: List[String] = []):
		self.run([ 'cmake', '--install', f'.build-{config}' ] + opts)

	# Odin helpers
	def odin_compile(self: Self, config: String, opts: List[String] = []):
		if config == 'release' or not Build.is_dev(config):
			OFLAGS = [ '-o:speed', '-no-bounds-check', '-disable-assert' ]
			if platform.system() == 'Windows':
				if config == 'internal':
					OFLAGS.append('-resource:res-internal.rc')
				else:
					OFLAGS.append('-resource:res.rc')
				OFLAGS.append('-subsystem:windows')

			if not Build.is_dev(config):
				OFLAGS.append('-define:SHIPPING=true')

			if config == 'internal':
				OFLAGS.append('-define:INTERNAL=true')
				githash = self.exec(True, [ 'git', 'rev-parse', '--short', 'HEAD' ])
				if not githash: raise Error('Could not determine git hash')
				status_bar_version = f'{datetime.today().strftime("%Y-%m-%d")}-{githash.strip()}'
				OFLAGS.append(f'-define:STATUS_BAR_VERSION={status_bar_version}')
				OFLAGS.append('-debug')
				if platform.system() == 'Windows':
					OFLAGS.append('-extra-linker-flags:/ignore:4099')
		elif config == 'debug':
			OFLAGS = [ '-o:none', '-debug' ]
			# When linking debug builds on Windows we ignore warning LNK4009:
			# PDB '' was not found with '' or at ''; linking object as if no debug info
			if platform.system() == 'Windows':
				OFLAGS.append('-extra-linker-flags:/ignore:4099')
		elif config == 'quick':
			# This is essentially just "Odin build ." which is implied
			OFLAGS = []

		# On Linux we always statically link libgcc
		if platform.system() == 'Linux':
			OFLAGS.append('-extra-linker-flags:-static-libgcc')

		if platform.system() == 'Darwin':
			OFLAGS.append('-error-pos-style:unix')

		environ = { 'CONSOLE': '1' }
		if self.config('color'):
			environ['ODIN_TERMINAL'] = 'ansi'

		odin_config = self.config('odin')
		odin_exe = odin_config['exe']
		odin_opt = odin_config['opt'][config]
		self.run([ odin_exe, 'build', '.', '-show-timings', *OFLAGS, *opts, *odin_opt ], environ)

	def odin_check(self: Self, config: String, opts: List[String] = []):
		# When running Odin check the type of build matters since release/non-dev
		# builds exclude some asserts and have conditional code. We want to ensure
		# those are set when running the type checker.
		if config == 'release' or not Build.is_dev(config):
			OFLAGS = [ '-disable-assert' ]
			if not Build.is_dev(config):
				OFLAGS.append('-define:SHIPPING=true')
		else:
			OFLAGS = []

		environ = { 'CONSOLE': '1' }
		if self.config('color'):
			environ['ODIN_TERMINAL'] = 'ansi'

		odin_config = self.config('odin')
		odin_exe = odin_config['exe']
		odin_opt = odin_config['opt']['check']
		self.run([ odin_exe, 'check', '.', '-show-timings', *OFLAGS, *opts, *odin_opt ], environ)

	def macos_package(self: Self, product: String, executable: String):
		print('Bundling macos app')

		version = self.semver()
		version = version.split('-')[0]

		app_folder = product + '.app'
		ICON_FILE = 'icon.icns'
		ICON_FINDER_FILE = 'file_icon.icns'
		if not os.path.exists(ICON_FINDER_FILE):
			ICON_FINDER_FILE = ICON_FILE

		self.log('[+] Bundling macOS app')
		app_folder = f'{product}.app'
		app_content_folder = os.path.join(app_folder, 'Contents')
		app_executable_folder = os.path.join(app_content_folder, 'MacOS')
		app_resource_folder = os.path.join(app_content_folder, 'Resources')
		self.rmdir(app_folder)

		self.mkdir(app_folder)
		self.mkdir(app_executable_folder)
		self.mkdir(app_resource_folder)
		self.cp(executable, app_executable_folder)

		self.cp(ICON_FILE, app_resource_folder)
		self.cp(ICON_FINDER_FILE, app_resource_folder)

		plist = PList()
		dict = plist.subelement('dict')
		dict.write('CFBundleInfoDictionaryVersion', '6.0')
		dict.write('CFBundleIconFile', ICON_FILE)
		dict.write('CFBundleIdentifier', f'com.jangafx.{product}')
		dict.write('CFBundleName', product)
		dict.write('CFBundleExecutable', executable)
		dict.write('CFBundlePackageType', 'APPL')
		dict.write('CFBundleShortVersionString', version)
		dict.write('CFBundleVersion', version)
		dict.write(f'NSHumanReadableCopyright', f'© 2016-{datetime.now().year} JangaFX. All rights reserved.')
		dict.write('LSMinimumSystemVersion', '15.0')
		dict.write('NSPrincipalClass', 'NSApplication')
		dict.write('CFBundleSupportedPlatforms', ['MacOSX'])
		dict.write('NSHighResolutionCapable', True)

		# File associations
		dict.write('CFBundleDocumentTypes', None)
		file_types = dict.subelement('array')
		file_dict = file_types.subelement('dict')
		file_dict.write('CFBundleTypeIconFile', ICON_FINDER_FILE)
		file_dict.write('CFBundleTypeName', f'{product} File')
		file_dict.write('CFBundleTypeOSTypes', ['****'])
		file_dict.write('CFBundleTypeRole', 'Editor')
		file_dict.write('LSIsAppleDefaultForType', True)
		file_dict.write('LSItemContentTypes', [f'com.jangafx.{product}.file'])
		file_dict.write('CFBundleTypeIconSystemGenerated', ICON_FINDER_FILE == ICON_FILE)
		file_dict.write('CFBundleTypeExtensions', [executable])

		# Export documents
		dict.write('UTExportedTypeDeclarations', None)
		file_types = dict.subelement('array')
		file_dict = file_types.subelement('dict')
		file_dict.write('UTTypeConformsTo', ['public.data'])
		file_dict.write('UTTypeIdentifier', f'com.jangafx.{product}.file')
		file_dict.write('UTTypeDescription', f'{product} File')

		file_dict.write('UTTypeIcons', None)
		icon_dict = file_dict.subelement('dict')
		icon_dict.write('UTTypeIconName', f'{product} File')
		icon_dict.write('UTTypeIconText', executable)

		file_dict.write('UTTypeTagSpecification', None)
		tag_dict = file_dict.subelement('dict')
		tag_dict.write('public.filename-extension', [executable])


		result = plist.render()
		with open(os.path.join(app_content_folder, 'Info.plist'), 'w') as f:
			f.write(result)

	def semver(self: Self):
		result = '0.0.0'
		with open(os.path.join('version', 'version.odin')) as f:
			lines = f.readlines()
			version = { 'Major': '', 'Minor': '', 'Patch': '', 'Build': '', }
			for line in lines:
				parts = line.strip().split()
				if len(parts) > 2 and parts[1] == '=':
					version[parts[0]] = parts[2][:-1]
			result = f"{version['Major']}.{version['Minor']}.{version['Patch']}"
			if version['Build'][1:-1]:
				result += f"-{version['Build'][1:-1]}"
		return result

	def PATH(self: Self, sys = True) -> String:
		paths = []
		# We have a faux chroot which we call 'root'. When this exists add it to the
		# path first so we can execute binaries from there.
		bin_path = os.path.join(self.prefix, 'bin')
		if os.path.isdir(bin_path):
			paths.append(bin_path)
		# We also put our in-tree Odin in the path too so that 'odin' works.
		paths.append(os.path.join(self.root, 'Odin'))
		# We only append the sys paths if requested
		if sys:
			# On Windows we only need these paths.
			if platform.system() == 'Windows':
				root = os.environ['SystemRoot']
				paths.append(root)
				paths.append(os.path.join(root, 'System32'))
				paths.append(os.path.join(root, 'System32', 'Wbem'))
				paths.append(os.path.join('C:\\', 'msys64', 'usr', 'bin'))
			else:
				# POSIX platforms usually have:
				#   /bin
				#   /usr/bin
				#   /usr/local/bin
				#
				# Most Linux distributions have since merged /bin with /usr/bin though, so
				# don't bother adding it to the path if it's a symlink to that. We still
				# add it if it's a symlink to somewhere else though.
				if not os.path.islink('/bin') or os.readlink('/bin') != '/usr/bin':
					paths.append('/bin')
				if os.path.isdir('/usr/bin'):
					paths.append('/usr/bin')
				if os.path.isdir('/usr/local/bin'):
					paths.append('/usr/local/bin')
		return os.pathsep.join(paths)

	def ENV(self: Self) -> Map[String, String]:
		environ = {}
		environ['PATH'] = self.PATH()
		environ['USER'] = 'JangaFX'
		environ['TERM'] = 'xterm'
		if platform.system() == 'Windows':
			environ['USERNAME'] = 'JangaFX'
			COPIED = [
				'PROCESSOR_ARCHITECTURE',
				'ProgramData',
				'ProgramFiles',
				'ProgramFiles(x86)',
				'CommonProgramFiles',
				'CommonProgramFiles(x86)',
				'APPDATA',
				'LOCALAPPDATA',
				'PATHEXT',
				'SystemDrive',
				'SystemRoot',
				'HOMEDRIVE',
				'HOMEPATH',
				'USERPROFILE',
				'TEMP',
				'TMP',
				'OS',
			]
			for name in COPIED:
				environ[name] = os.environ[name]
		return environ

	def __init__(self: Self, targets: List[Type[Target]]):
		self.root = os.path.abspath('..')

		self.load_config()

		# Work out the relative prefix for our root.
		prefix = None
		if platform.system() == 'Linux':
			prefix = os.path.join('root', 'lin')
		elif platform.system() == 'Darwin':
			prefix = os.path.join('root', 'mac')
		elif platform.system() == 'Windows':
			prefix = os.path.join('root', 'win')
		else:
			raise Error(f'Unsupported platform: {platform.system()}')

		# Setup the FHS:
		# 	https://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard
		self.prefix = os.path.abspath(prefix)
		self.fhs = [
			os.path.join(prefix, 'bin'),
			os.path.join(prefix, 'doc'),
			os.path.join(prefix, 'share'),
			os.path.join(prefix, 'man'),
			os.path.join(prefix, 'include'),
		]
		# Ensure they all exist
		for path in self.fhs:
			self.mkdir(path)

		def ENV() -> Map[String, String]:
			return self.ENV()

		self.environ = [ENV]
		self.targets = {}
		self.progress = Progress(self.config('quiet'))
		self.writable = set()
		self.toolchain = Toolchain(self.prefix)

		# The '__exit__' method also removes the '.tmp' directory but it's possible
		# Python was killed or we suffered power-loss before this method could run.
		# Having a stale '.tmp' directory could be a problem so on init make sure we
		# purge it too.
		self.rmtree('.tmp')

		# Likewise ensure the prefix exists too.
		self.mkdir(self.prefix)

		for target in targets:
			# Target has an __init__ with multiple arguments but here we're given only
			# derived class types which have an implicit generated '__init__' provided
			# by the 'target' decorator with no arguments. Let the linters know that
			# the callable takes no arguments with a cast.
			instance = typing.cast(Callable[[], Target], target)()
			self.targets[instance.name] = instance

		# Reset the log when no checkpoint found or we're fresh
		if not self.load_checkpoint() or self.fresh():
			self.logfile = open(self.config('log'), 'wb')
		else:
			self.logfile = open(self.config('log'), 'ab')
		self.loglock = threading.Lock()

		# Check that the dependencies make sense for each target
		for name in self.targets:
			targ = self.targets[name]
			for dep in targ.deps:
				if dep not in self.targets:
					raise Error(f'Unknown dependency "{dep}" in target "{name}"\n'
					            f'  There is no target named "{dep}" in the Build instance')

		# Ensure a checkpoint entry exists for each target and that an entry exists
		# for each stage of the build.
		for name in self.targets:
			key = self.targets[name].key()
			if key not in self.cpdata['targets']:
				self.cpdata['targets'][key] = {
					'unpack':    { 'tracked': [], 'reached': False, 'timestamp': 0 },
					'configure': { 'tracked': [], 'reached': False, 'timestamp': 0 },
					'compile':   { 'tracked': [], 'reached': False, 'timestamp': 0 },
					'install':   { 'tracked': [], 'reached': False, 'timestamp': 0 }
				}

	# The Build class is supposed to be used in a with statement since we want to
	# sync the checkpoint state to disk for any reason, including exceptions.
	def __enter__(self: Self) -> Self:
		return self
	def __exit__(self:      Self,
	             type:      Optional[Type[BaseException]],
	             value:     Optional[BaseException],
	             traceback: Optional[TracebackType]) -> Optional[Bool]:
		if type is None:
			self.progress.done('✓')
		else:
			self.progress.done('✕')
		self.save_checkpoint()
		self.save_config()

		# Ensure we never leave the tmp directory around.
		self.rmtree('.tmp')

		# When we have a fresh structure (initial, or clean)
		if self.fresh():
			# Remove any extracted src packages if there are any.
			self.rmtree('.src')
			# Remove the FHS and our prefix
			for path in self.fhs:
				self.rmtree(path)
			self.rmdir(self.prefix)
			self.rmdir('root')

		return None

	def fresh(self: Self):
		# Considered fresh when all stages of all targets have not been reached.
		for name in self.targets:
			for stage in [ 'unpack', 'configure', 'compile', 'install' ]:
				checkpoint = self.checkpoint(self.targets[name], stage)
				if checkpoint['reached']:
					return False
		return True

	def usage(self: Self, msg: String, app: String):
		raise Error(('{0}Usage: {1} action config [target...]\n'
		             '{2}Actions:\n'
		             '{3}build\n'
		             '{3}clean\n'
		             '{3}rebuild\n'
		             '{3}check\n'
		             '{3}run\n'
		             '{3}project\n'
		             '{2}Configs:\n'
		             '{3}debug\n'
		             '{3}quick\n'
		             '{3}release\n'
		             '{3}internal\n'
		             '{3}shipping\n'
		             '{2}Targets:\n'
		             '{3}{4}').format(f'{msg}\n' if msg else '', app, ' '*2, ' '*4, ('\n'+' '*4).join(self.targets)))

	def go(self: Self, args: List[String]):
		app = 'make' if os.environ.get('MAKELEVEL') else args[0]
		if len(args) <= 2:
			self.usage('', app)
		if args[1] == 'project':
			# TODO(dweiler): Other project generators (vscode/zed/etc)?
			editor = args[2]
			if editor != "sublime" and editor != "vscode":
				self.usage(f'Unknown editor "{editor}"\n'
				           f'  There is no editor named "{editor}"', app)
				return
			targets = args[3:] if len(args) > 3 else list(self.targets.keys())
			for target in targets:
				if target not in self.targets:
					self.usage(f'Unknown target "{target}"\n'
					           f'  There is no target named "{target}"', app)
				elif isinstance(self.targets[target], Product):
					self.do_project(editor, target)
			return

		# app build release embergen (4 arguments)
		cmd = getattr(self, f'do_{args[1]}', None)
		if cmd:
			config = args[2]
			if config != 'debug' and config != 'quick' and config != 'release' and Build.is_dev(config):
				self.usage(f'Unknown config "{config}"\n'
				           f'   Expected either "debug", "quick", "release", "internal", or "shipping"', app)
			self.cpdata['history'].append(' '.join(args[1:]))
			targets = args[3:] if len(args) > 3 else list(self.targets.keys())
			for target in targets:
				if target not in self.targets:
					self.usage(f'Unknown target "{target}"\n'
					           f'  There is no target named "{target}"', app)
			order = []
			if args[1] == 'build' or args[1] == 'rebuild':
				# Topological sort based on dependencies for (re)?builds.
				stack = []
				visit = set()
				for target in targets:
					if target in visit:
						continue
					stack.append((target, False))
					while stack:
						node, done = stack.pop()
						if done:
							order.append(node)
							visit.add(node)
							continue
						if node in visit:
							continue
						stack.append((node, True))
						for dep in reversed(self.targets[node].deps):
							if dep not in visit:
								stack.append((dep, False))
			else:
				# No need to sort anything for most other commands.
				order.extend(targets)
			for target in order:
				cmd(target, self.targets[target].config(config))
		else:
			self.usage(f'Unknown action: "{args[1]}"', app)

	CONFIG = 'config.cfg'
	CHECKPOINT = '.checkpoint.pkl'

	def load_config(self: Self) -> Bool:
		ODIN_DEFAULT_EXE = os.path.realpath(os.path.join('..', 'Odin', 'odin'))
		ODIN_DEFAULT_OPT_LIST = [ '-use-separate-modules', '-terse-errors' ]
		ODIN_DEFAULT_OPT_CHECK_LIST = [ '-terse-errors' ]
		ODIN_DEFAULT_OPT = {
			'debug':    ODIN_DEFAULT_OPT_LIST,
			'quick':    ODIN_DEFAULT_OPT_LIST,
			'release':  ODIN_DEFAULT_OPT_LIST,
			'internal': ODIN_DEFAULT_OPT_LIST,
			'shipping': ODIN_DEFAULT_OPT_LIST,
			'check':    ODIN_DEFAULT_OPT_CHECK_LIST,
		}
		ODIN_DEFAULT_OBJ = {
			'exe': ODIN_DEFAULT_EXE,
			'opt': ODIN_DEFAULT_OPT
		}
		default = max(os.cpu_count() or 0, 4)
		try:
			self.configs = []
			with open(self.CONFIG, 'r') as fp:
				config = json.load(fp)
				if not 'jobs' in config or not isinstance(config['jobs'], int):
					config['jobs'] = default
				if not 'log' in config or not isinstance(config['log'], str):
					config['log'] = 'log.log'
				if not 'odin' in config or not isinstance(config['odin'], dict):
					config['odin'] = {}
				if not 'color' in config or not isinstance(config['color'], bool):
					config['color'] = True
				if not 'quiet' in config or not isinstance(config['quiet'], bool):
					config['quiet'] = False
				if not 'lock' in config or not isinstance(config['lock'], list):
					config['lock'] = []
				if not 'exe' in config['odin'] or not isinstance(config['odin']['exe'], str):
					config['odin']['exe'] = ODIN_DEFAULT_EXE
				if not 'opt' in config['odin'] or not isinstance(config['odin']['opt'], dict):
					config['odin']['opt'] = ODIN_DEFAULT_OPT
				if not 'debug' in config['odin']['opt'] or not isinstance(config['odin']['opt']['debug'], list):
					config['odin']['opt']['debug'] = ODIN_DEFAULT_OPT_LIST
				if not 'quick' in config['odin']['opt'] or not isinstance(config['odin']['opt']['quick'], list):
					config['odin']['opt']['quick'] = ODIN_DEFAULT_OPT_LIST
				if not 'release' in config['odin']['opt'] or not isinstance(config['odin']['opt']['release'], list):
					config['odin']['opt']['release'] = ODIN_DEFAULT_OPT_LIST
				if not 'internal' in config['odin']['opt'] or not isinstance(config['odin']['opt']['internal'], list):
					config['odin']['opt']['internal'] = ODIN_DEFAULT_OPT_LIST
				if not 'shipping' in config['odin']['opt'] or not isinstance(config['odin']['opt']['shipping'], list):
					config['odin']['opt']['shipping'] = ODIN_DEFAULT_OPT_LIST
				if not 'check' in config['odin']['opt'] or not isinstance(config['odin']['opt']['check'], list):
					config['odin']['opt']['check'] = ODIN_DEFAULT_OPT_CHECK_LIST
				self.configs.append(config)

			# The environment variables take precedence over the config if present.
			quiet = os.environ.get('JFX_BUILD_QUIET', None)
			color = os.environ.get('JFX_BUILD_COLOR', None)
			if quiet and isinstance(quiet, str):
				self.configs.append({ **self.configs[-1].copy(), 'quiet': int(quiet, 10) != 0 })
			if color and isinstance(color, str):
				self.configs.append({ **self.configs[-1].copy(), 'color': int(color, 10) != 0 })
			return True
		except (FileNotFoundError, json.JSONDecodeError):
			self.configs = [{
				'jobs':  default,
				'log':   'log.log',
				'color': True,
				'quiet': False,
				'odin':  ODIN_DEFAULT_OBJ,
				'lock':  []
			}]
			return False

	def save_config(self: Self):
		tmp = f'{self.CONFIG}.tmp'
		with open(tmp, 'w') as fp:
			json.dump(self.configs[0], fp, indent=2)
		self.mv(tmp, self.CONFIG)

	def load_checkpoint(self: Self) -> Bool:
		pkl = self.CHECKPOINT.endswith('.pkl')
		try:
			with open(self.CHECKPOINT, 'rb' if pkl else 'r') as fp:
				if pkl:
					self.cpdata = pickle.load(fp)
				else:
					self.cpdata = json.load(fp)
			return True
		except (FileNotFoundError, pickle.PickleError, json.JSONDecodeError):
			self.cpdata = { 'history': [], 'targets': {} }
			return False

	def save_checkpoint(self: Self):
		tmp = f'{self.CHECKPOINT}.tmp'
		pkl = self.CHECKPOINT.endswith('.pkl')
		with open(tmp, 'wb' if pkl else 'w') as fp:
			if pkl:
				pickle.dump(self.cpdata, fp)
			else:
				json.dump(self.cpdata, fp, indent=2)
		self.mv(tmp, self.CHECKPOINT)

	def do_build(self: Self, name: String, config: String):
		target = self.targets[name]
		# Bundles require unpacking a selected package.
		if isinstance(target.kind, Bundle):
			self.unpack(target, config)
		self.configure(target, config)
		self.compile(target, config)
		self.install(target, config)
		self.save_checkpoint()

	def do_clean(self: Self, name: String, config: String):
		target = self.targets[name]
		self.progress.reset(f'Cleaning    | {name}')
		if name in self.config('lock'):
			wait = input(f'\n  The "{name}" package has been locked to prevent accidentally cleaning it.\n  Cleaning it will require recompiling it from source.\n  Are you sure you want to clean it? (Y/n): ')
			if wait.lower() != 'y':
				self.progress.skip()
				return
		self.cleanup(target, config, 'install')
		self.cleanup(target, config, 'compile')
		self.cleanup(target, config, 'configure')
		self.cleanup(target, config, 'unpack')

	def do_rebuild(self: Self, name: String, config: String):
		self.do_clean(name, config)
		self.do_build(name, config)

	def do_check(self: Self, name: String, config: String):
		target = self.targets[name]
		if isinstance(target, Product):
			self.progress.reset(f'Checking    | {target.name}')
			with pushd(target.src_path()):
				target.check(config, self)
		else:
			raise Error('Cannot check: {name}. Only products can be checked.')

	def do_run(self: Self, name: String, config: String):
		target = self.targets[name]
		if isinstance(target, Product):
			self.do_rebuild(name, config)
			self.progress.reset(f'Running     | {name}')
			with pushd(target.src_path()):
				self.run([os.path.join('.', os.path.basename(target.src_path()))], {**os.environ, 'CONSOLE': '1'})
		else:
			raise Error('Cannot run: {name}. Only products can be run.')

	def do_project(self: Self, editor: String, name: String):
		# Create a Sublime project file for this product
		path = os.path.relpath(self.targets[name].src_path(), '..')
		project: Optional[Union[Sublime, VSCode]] = None
		if editor == 'sublime':
			project = Sublime(name, path)
		elif editor == 'vscode':
			project = VSCode(name, path)
		else:
			return
		for action in [ 'build', 'run' ]:
			capitalized = action.capitalize()
			project.add_config(f'Quick {capitalized}', action, 'quick')
			project.add_config(f'Debug {capitalized}', action, 'debug')
			project.add_config(f'Release {capitalized}', action, 'release')
			project.add_config(f'Internal {capitalized}', action, 'internal')
			project.add_config(f'Shipping {capitalized}', action, 'shipping')
		# Exclude all other targets in the project file except ourselves.
		for key in self.targets:
			target = self.targets[key]
			if isinstance(target, Product) and key != name:
				project.add_folder_exclude(os.path.relpath(target.src_path(), '..'))
		project.save('..')

	def checkpoint(self: Self, target: Target, stage: String):
		return self.cpdata['targets'][target.key()][stage]

	def modified(self: Self, checkpoint, target: Target) -> Bool:
		# When target.date = False it means we always assume the target is out of
		# date.
		if not target.date:
			self.log(f'[+] Rebuilding "{target.name}" since marked out of date"')
			return True
		# Use multiple threads to check if a file has been deleted or modified since
		# this is also where the rubber meets the road.
		def check(files, timestamp):
			result = []
			for file in files:
				try:
					info = os.stat(file)
					# Filter out directories when checking
					if stat.S_ISDIR(info.st_mode):
						result.append((file, False, False))
					else:
						result.append((file, False, info.st_mtime > timestamp))
				except FileNotFoundError:
					result.append((file, True, False))
				except KeyboardInterrupt:
					pass
			return result
		threads = int(self.config('jobs'))
		files = checkpoint['tracked']
		files_per_batch = (len(files) + threads - 1) // threads
		batches = [files[i:i+files_per_batch] for i in range(0, len(files), max(1, files_per_batch))]
		with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as exec:
			timestamp = checkpoint['timestamp']
			futures = []
			for batch in batches:
				futures.append(exec.submit(check, batch, timestamp))
			for future in concurrent.futures.as_completed(futures):
				for result in future.result():
					if result[1]:
						self.log(f'[+] Rebuilding "{target.name}" due to missing file "{result[0]}"')
						return True
					if result[2]:
						self.log(f'[+] Rebuilding "{target.name}" due to modification of "{result[0]}"')
						return True
			return False

	def itprogress(self: Self):
		def cb(i: Int, count: Int):
			self.progress.show(count, i)
		return cb

	def cleanup(self: Self, target: Target, config: String, stage: String):
		checkpoint = self.checkpoint(target, stage)
		tracked = checkpoint['tracked']
		self.rmseq(tracked, self.itprogress())
		checkpoint['tracked'] = []
		checkpoint['reached'] = False
		checkpoint['timestamp'] = 0

	# Filter out standard FHS paths from what is tracked.
	def tracked(self: Self, paths: List[String]):
		return list(filter(lambda path: path not in self.fhs, paths))

	# Unpack should only be called on Bundles
	def unpack(self: Self, target: Target, config: String):
		if not isinstance(target.kind, Bundle):
			return
		self.log(f'[+] Unpacking "{target.name}"')
		checkpoint = self.checkpoint(target, 'unpack')
		if checkpoint['reached']:
			self.log(f'[+] Skipped "{target.name}" \'unpack\' step due to checkpoint')
			return
		try:
			self.progress.reset(f'Unpacking   | {target.name}')
			pkg = target.kind.pkg_path()
			src = target.src_path()
			tmp = target.tmp_path()
			# Could be stale files left in the src or tmp directory for some reason.
			# To prevent unpack errors ensure those are non-existant.
			self.rmtree(src)
			self.rmtree(tmp)
			shutil.unpack_archive(pkg, tmp)
			# On macOS we want to remove all the quarantine attributes from all files
			# in here since Gatekeeper will prevent us from running an executable that
			# we did not create ourselves.
			if platform.system() == 'Darwin':
				self.run(['xattr', '-r', '-d', 'com.apple.quarantine', tmp])
			# We then look at the single top-level directory in tmp and move it to
			# target.src_path() to normalize the naming since we cannot know
			# the top level name that may be in the archive.
			self.mvtree(os.path.join(tmp, list(os.listdir(tmp))[0]),
			            src,
			            self.itprogress())
			checkpoint['reached'] = True
		except Exception as error:
			raise Error(f'Could not unpack: "{pkg}"\n'
			            f'  {error}')
		finally:
			# We only need to track the source directory.
			checkpoint['tracked'] = [ src ]
			checkpoint['timestamp'] = time.time()

	def stage(self: Self, target: Target, config: String, delta_paths: List[String], stage: String, label: String):
		self.log(f'[+] {label.strip()} "{target.name}"')
		checkpoint = self.checkpoint(target, stage)
		if checkpoint['reached'] and not self.modified(checkpoint, target):
			self.log(f'[+] Skipped "{target.name}" \'{stage}\' step due to checkpoint')
			return
		beg = {}
		try:
			src_path = target.src_path()
			self.progress.reset(f'{label} | {target.name}')
			beg = dict.fromkeys(list(lstrees(delta_paths, True)))
			with pushd(src_path):
				getattr(target, stage)(config, self)
			checkpoint['reached'] = True
		except Exception as error:
			self.log(f'Could not {stage}: {target.name} {error}\n' f'  {"".join(traceback.format_stack()[:-1])}')
			raise Error(f'Could not {stage}: {target.name} {error}')
		finally:
			# We always want to track the changes to the filesystem even in the face
			# of exceptions since we might need to cleanup that partial, inconsistent
			# state.
			end = list(lstrees(delta_paths))
			delta = [item for item in end if item not in beg]
			checkpoint['tracked'] = self.tracked(delta)
			checkpoint['timestamp'] = time.time()

	def configure(self: Self, target: Target, config: String):
		self.stage(target, config, [target.src_path()], 'configure', 'Configuring')
	def compile(self: Self, target: Target, config: String):
		self.stage(target, config, [target.src_path()], 'compile', 'Compiling  ')
	def install(self: Self, target: Target, config: String):
		self.stage(target, config, [target.src_path(), os.path.relpath(self.prefix, os.getcwd())], 'install', 'Installing ')

	def exec(self:    Self,
	         read:    Bool,
	         command: List[String],
	         environ: Optional[Map[String, String]] = None) -> Optional[String]:
		def cmdfail(command, status):
			msg = signal.strsignal(-status) if status < 0 else f'{status}'
			raise Error(f'Command "{" ".join(command)}" failed with: {msg}')

		path = shutil.which(command[0], path=self.PATH(False))
		if path:
			command[0] = path

		# Runs the command with arguments in such a way that the environment is not
		# exposed and logs the command to self.log.
		env = self.environ[-1]()
		if environ:
			env.update(environ)

		# Prepare and format the log header at once to avoid lock contention.
		header = []
		header.append(f'{"#"*80}')
		header.append('[+] Running command:')
		header.append('  CWD: {}'.format(os.getcwd()))
		header.append('  CMD: {}'.format(command))
		header.append('  ENV: {')
		for k in env:
			header.append(f'    {k} = {env[k]}')
		header.append('  }')
		self.log('\n'.join(header))
		try:
			result = subprocess.Popen(command,
			                          stdout=subprocess.PIPE,
			                          stderr=subprocess.STDOUT,
			                          env=env)
		except OSError as error:
			cmdfail(command, -error.errno if error.errno else -1)
		# As each line is outputted, append it to the log.
		output = []
		for line in io.TextIOWrapper(result.stdout, encoding='utf-8'): # type: ignore
			# Here we support [i/j] or [i%] for progress (Ninja and GNUMake)
			find = re.search(r'^\[\s*(\d+)(?:%|\/(\d+))\]', line)
			if find:
				groups = find.groups()
				self.progress.show(int(groups[1]) if groups[1] else 100, int(groups[0]))
			self.log(line.rstrip())
			if read:
				output.append(line)
			if env.get('CONSOLE', None):
				print(f'    {line.rstrip()}')
		status = result.wait()

		if status != 0:
			cmdfail(command, status)
		if read:
			return '\n'.join(output)
		return None

	def run(self: Self, command: List[String], environ: Optional[Map[String, String]] = None):
		self.exec(False, command, environ)

	def inline(self: Self, command: List[String], environ: Optional[Map[String, String]] = None) -> List[String]:
		exec = self.exec(True, command, environ)
		if exec:
			return shlex.split(exec, posix=platform.system() != 'Windows')
		else:
			return []

def target(cls: Type[Target]) -> Type[Target]:
	def init(cls: Target):
		name = getattr(cls, 'NAME', type(cls).__name__.lower())
		deps = getattr(cls, 'DEPS', [])
		urls = getattr(cls, 'URLS', [])
		ignr = getattr(cls, 'IGNR', [])
		date = getattr(cls, 'DATE', True)
		path = getattr(cls, 'PATH', None)
		Target.__init__(cls, name, deps, ignr, date, Project(name, path) if path else Bundle(name, urls))
	setattr(cls, '__init__', init)
	return cls

# Helper function that runs vswhere.exe (ships with the Visual Studio installer)
# to find the x86.x64 VC tools installation path. The installation path is then
# used to find the vsdevcmd.bat script which sets up all the right environment
# variables. We then execute the vsdevcmd.bat script inside a shell subprocess
# and run the SET command after it to dump all environment variables to stdout.
# We then parse the SET output to create a dict. This dict now contains an exact
# replica of the environment that vsdevcmd.bat would setup if manually invoked.
# We use this environment only during the LLVM configure phase on Windows. Once
# LLVM is built we no longer need it.
def vsinstall():
	return subprocess.check_output([
		os.path.join(os.environ['ProgramFiles(x86)'], 'Microsoft Visual Studio', 'Installer', 'vswhere.exe'),
		'-latest',
		'-products', '*',
		'-requires', 'Microsoft.VisualStudio.Component.VC.Tools.x86.x64',
		'-property', 'installationPath'
	]).decode('utf-8').strip()

def vsenviron():
	output = subprocess.check_output([
		os.path.join(vsinstall(), 'Common7', 'Tools', 'vsdevcmd.bat'),
		'-arch=x64',
		'-host_arch=x64',
		'&',
		'set'
	]).decode('utf-8').strip()
	environ = {}
	for line in output.splitlines():
		if '=' not in line:
			continue
		k, _, v = line.partition('=')
		environ[k] = v
	return environ

@target
class CMake(Target):
	@staticmethod
	def URL() -> Map[String, String]:
		CMAKE_URL = 'https://github.com/Kitware/CMake/releases/download'
		if platform.system() == 'Windows':
			return {
				'src': f'{CMAKE_URL}/v{CMAKE_VERSION}/cmake-{CMAKE_VERSION}-windows-x86_64.zip',
				'dst': f'cmake-{CMAKE_VERSION}.zip'
			}
		elif platform.system() == 'Linux':
			return {
				'src': f'{CMAKE_URL}/v{CMAKE_VERSION}/cmake-{CMAKE_VERSION}-linux-x86_64.tar.gz',
				'dst': f'cmake-{CMAKE_VERSION}.tar.gz'
			}
		elif platform.system() == 'Darwin':
			return {
				'src': f'{CMAKE_URL}/v{CMAKE_VERSION}/cmake-{CMAKE_VERSION}-macos-universal.tar.gz',
				'dst': f'cmake-{CMAKE_VERSION}.tar.gz',
			}
		else:
			raise Error(f'Unknown platform: "{platform.system()}"')
	URLS = [ URL.__get__(Target)() ] # This is unfortunute.
	def configure(self: Self, config: String, build: Build):
		pass
	def compile(self: Self, config: String, build: Build):
		pass
	def install(self: Self, config: String, build: Build):
		# On macOS when extracting the macos-universal.tar.gz we have the standard
		# CMake.app/Contents structure and we really do not want that. Our prefix
		# is the standard Unix prefix so lets fix that.
		if platform.system() == 'Darwin':
			build.cptree(os.path.join('CMake.app', 'Contents'), build.prefix)
		else:
			build.cptree('.', build.prefix)

@target
class Ninja(Target):
	DEPS = [ 'cmake' ]
	def configure(self: Self, config: String, build: Build):
		# When compiling Ninja we cannot depend on Ninja
		build.run([
			'cmake',
			'-Wno-dev',
			'-B', '.build-{}'.format(config),
			'-DBUILD_TESTING=OFF',
			'-DCMAKE_WARN_DEPRECATED=OFF',
			'-DCMAKE_INSTALL_PREFIX={}'.format(build.prefix),
			'-DCMAKE_PREFIX_PATH={}'.format(build.prefix),
			'-DCMAKE_POSITION_INDEPENDENT_CODE=ON',
		])
	def compile(self: Self, config: String, build: Build):
		build.run([
			'cmake',
			'--build', f'.build-{config}',
			'--config', 'Release' if config == 'release' else 'Debug',
			'--parallel', str(build.config('jobs')),
			'--verbose'
		])

@target
class LLVM(Target):
	DEPS = [ 'cmake', 'ninja' ]
	URLS = [
		{
			'src': f'https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-{LLVM_VERSION}.zip',
			'dst': f'llvm-{LLVM_VERSION}.zip'
		}
	]
	def configure(self: Self, config: String, build: Build):
		FLAGS = [
			'-DLLVM_APPEND_VC_REF=OFF',
			'-DLLVM_ENABLE_PROJECTS=clang;lld;compiler-rt',
			'-DLLVM_TARGETS_TO_BUILD=AArch64;WebAssembly;X86',
			'-DLLVM_BUILD_LLVM_C_DYLIB=OFF',
			'-DLLVM_ENABLE_BACKTRACES=OFF',
			'-DLLVM_ENABLE_UNWIND_TABLES=OFF',
			'-DLLVM_ENABLE_CRASH_OVERRIDES=OFF',
			'-DLLVM_ENABLE_CRASH_DUMPS=OFF',
			'-DLLVM_ENABLE_TERMINFO=OFF',
			'-DLLVM_ENABLE_LIBXML2=OFF',
			'-DLLVM_ENABLE_LIBEDIT=OFF',
			'-DLLVM_ENABLE_LIBPFM=OFF',
			'-DLLVM_ENABLE_ZLIB=OFF',
			'-DLLVM_ENABLE_ZSTD=OFF',
			'-DLLVM_ENABLE_CURL=OFF',
			'-DLLVM_ENABLE_HTTPLIB=OFF',
			'-DLLVM_ENABLE_Z3_SOLVER=OFF',
			'-DLLVM_ENABLE_WARNINGS=OFF',
			'-DLLVM_ENABLE_PEDANTIC=OFF',
			'-DLLVM_ENABLE_WERROR=OFF',
			'-DLLVM_ENABLE_ASSERTIONS=OFF',
			'-DLLVM_BUILD_EXAMPLES=OFF',
			'-DLLVM_BUILD_TESTS=OFF',
			'-DLLVM_BUILD_BENCHMARKS=OFF',
			'-DLLVM_BUILD_DOCS=OFF',
			'-DLLVM_INCLUDE_EXAMPLES=OFF',
			'-DLLVM_INCLUDE_TESTS=OFF',
			'-DLLVM_INCLUDE_BENCHMARKS=OFF',
			'-DLLVM_INCLUDE_DOCS=OFF',
			'-DLLVM_ENABLE_OCAMLDOC=OFF',
			'-DLLVM_ENABLE_BINDINGS=OFF',
			'-DLLVM_ENABLE_PLUGINS=OFF',
			'-DLLVM_ENABLE_IDE=OFF',
			'-DCLANG_BUILD_EXAMPLES=OFF',
			'-DCLANG_INCLUDE_TESTS=OFF',
			'-DCLANG_INCLUDE_DOCS=OFF',
			'-DCLANG_ENABLE_ARCMT=OFF',
			'-DCLANG_ENABLE_STATIC_ANALYZER=OFF',
			'-DCLANG_DEFAULT_LINKER=lld',
			'-DCOMPILER_RT_BUILD_SANITIZERS=ON',
			'-DCOMPILER_RT_BUILD_LIBFUZZER=ON',
			'-DCOMPILER_RT_BUILD_PROFILE=ON',
			'-DCOMPILER_RT_BUILD_BUILTINS=OFF',
			'-DCOMPILER_RT_BUILD_XRAY=OFF',
			'-DCOMPILER_RT_BUILD_MEMPROF=OFF',
			'-DCOMPILER_RT_BUILD_XRAY_NO_PREINIT=OFF',
			'-DCOMPILER_RT_BUILD_ORC=OFF',
			'-DCOMPILER_RT_BUILD_GWP_ASAN=OFF',
			'-DCOMPILER_RT_ENABLE_CET=OFF',
		]
		# MacOS SDKs live outside of our local LLVM build, have our build be able to find them
		if platform.system() == 'Darwin':
			FLAGS.append(f"-DDEFAULT_SYSROOT={' '.join(build.inline(['xcrun', '--show-sdk-path']))}")
		if platform.system() == 'Windows':
			with build.env(vsenviron()):
				build.cmake_configure(config, [*FLAGS, 'llvm'])
		else:
			build.cmake_configure(config, [*FLAGS, 'llvm'])

	def compile(self: Self, config: String, build: Build):
		if platform.system() == 'Windows':
			with build.env(vsenviron()):
				build.cmake_compile(config)
		else:
			build.cmake_compile(config)

	def install(self: Self, config: String, build: Build):
		build.cmake_install(config)
		if platform.system() == 'Windows':
			# Odin assumes LLVM is built just for LLVM-C to read the config but we
			# build the whole thing and so we need to make a copy of the llvm-config.h
			src_cfg = os.path.join(build.prefix, 'include', 'llvm', 'Config')
			dst_cfg = os.path.join(build.prefix, 'include', 'llvm-c', 'Config')
			build.mkdir(dst_cfg)
			build.cp(os.path.join(src_cfg, 'llvm-config.h'),
			         os.path.join(dst_cfg, 'llvm-config.h'))
		# We'll also install a custom config for the toolchain to setup our sysroot
		# and provide default compiler options that should be used regardless.
		for file in ['clang.cfg', 'clang++.cfg']:
			with open(os.path.join(build.prefix, 'bin', file), 'w') as cfg:
				# We don't want any warnings in our log.
				cfg.write('-Wno-everything\n')
				# This is our isysroot for includes. Normally we'd use -isysroot here
				# but clang does not support that, so just add it regularly. Since these
				# config files are always loaded first, this always comes first.
				cfg.write(f'-I{os.path.join(build.prefix, "include")}\n')
				if platform.system() != 'Darwin':
					# Toolchain will pick no later than SSE2 but we want something newer.
					# Not needed on Darwin since that's AArch64.
					cfg.write('-msse4.2\n')
				# LTO: cfg.write('-flto\n')
				# LTO: cfg.write('-ffat-lto-objects\n')
		# Custom config for clang-cl due to the different command line options.
		with open(os.path.join(build.prefix, 'bin', 'clang-cl.cfg'), 'w') as cfg:
			# Some code incorrectly checks for WIN32 instead of _WIN32. MSVC actually
			# defines both but clang-cl doesn't.
			cfg.write('/DWIN32\n')
			# Standard C++ exception handling but no SEH because clang-cl does not
			# support asynchronous exceptions.
			cfg.write('/EHsc\n')
			# We don't want any warnings in our log.
			cfg.write('/W0\n')
			# We don't want the buffer security checks.
			cfg.write('/GS-\n')
			# This is our isystroot for includes.
			cfg.write(f'/I{os.path.join(build.prefix, "include").replace(os.sep, "/")}\n')
			# Since clang-cl tries to be compatible with cl.exe (i.e MSVC) it also
			# disables TBAA (type based alias analysis) which is a useful optimization
			# that we actually want. OpenEXR claims about ~12% performance difference
			# with this flag alone so we should probably enable it.
			cfg.write('/clang:-fstrict-aliasing\n')
			cfg.write('/clang:-msse4.2\n')
			# LTO: cfg.write('/clang:-flto\n')
			# LTO: cfg.write('/clang:-ffat-lto-objects\n')

		# Once LLVM is installed we will add it to the lock.
		build.configs[0]['lock'].append('llvm')

@target
class STBImage(Target):
	DEPS = [ 'llvm', 'cmake', 'ninja' ]
	NAME = 'stb-image'

@target
class STBImageWrite(Target):
	DEPS = [ 'llvm', 'cmake', 'ninja' ]
	NAME = 'stb-image-write'

@target
class ZLib(Target):
	DEPS = [ 'llvm', 'cmake', 'ninja' ]
	# Zlib has an unusual build step where the source package contains a default
	# configuration header named 'zconf.h'. During CMake configure, this header is
	# copied to the CMake build directory and modified and then deleted from the
	# source directory. This is problematic because our build system captures a
	# delta of all source files after the unpack step and saves them to know if a
	# file has gone missing, or has been edited the next time the build is run. If
	# it cannot find the 'zconf.h' file it will trigger a rebuild which we don't
	# want. Here we can use the "ignore" feature of the build system to provide a
	# regular expression of specific file patterns we'd like to ignore.
	IGNR = [ r'^.*zconf.h$' ]
	def configure(self: Self, config: String, build: Build):
		build.cmake_configure(config, [
			'-DZLIB_BUILD_EXAMPLES=OFF',
			'-DZLIB_BUILD_TESTING=OFF'
			'-DZLIB_BUILD_SHARED=OFF',
			'-DZLIB_BUILD_STATIC=ON',
		])
	def install(self: Self, config: String, build: Build):
		build.cmake_install(config)
		if platform.system() == 'Windows':
			# Remove the zlib.lib and rename zlibstatic.lib to zlib.lib.
			dst = os.path.join(build.prefix, 'lib', 'zlib.lib')
			src = os.path.join(build.prefix, 'lib', 'zlibstatic.lib')
			build.rm(dst)
			build.mv(src, dst)

@target
class MBedTLS(Target):
	DEPS = [ 'llvm', 'cmake', 'ninja' ]
	def configure(self: Self, config: String, build: Build):
		build.cmake_configure(config, [
			'-DENABLE_PROGRAMS=OFF',
			'-DENABLE_TESTING=OFF'
		])

@target
class Curl(Target):
	DEPS = [ 'llvm', 'cmake', 'ninja', 'mbedtls', 'zlib' ]
	def configure(self: Self, config: String, build: Build):
		build.cmake_configure(config, [
			'-DBUILD_CURL_EXE=OFF',
			'-DBUILD_LIBCURL_DOCS=OFF',
			'-DENABLE_UNICODE=ON',
			'-DENABLE_THREADED_RESOLVER=ON',
			'-DENABLE_UNIX_SOCKETS=OFF',
			'-DCURL_DISABLE_ALTSVC=ON',
			'-DCURL_DISABLE_DOH=ON',
			'-DCURL_DISABLE_FILE=ON',
			'-DCURL_DISABLE_FTP=ON',
			'-DCURL_DISABLE_GOPHER=ON',
			'-DCURL_DISABLE_HSTS=ON',
			'-DCURL_DISABLE_IMAP=ON',
			'-DCURL_DISABLE_LDAP=ON',
			'-DCURL_DISABLE_LDAPS=ON',
			'-DCURL_DISABLE_MQTT=ON',
			'-DCURL_DISABLE_NETRC=ON',
			'-DCURL_DISABLE_NTLM=ON',
			'-DCURL_DISABLE_DICT=ON',
			'-DCURL_DISABLE_PARSEDATE=ON',
			'-DCURL_DISABLE_POP3=ON',
			'-DCURL_DISABLE_PROXY=ON',
			'-DCURL_DISABLE_RTSP=ON',
			'-DCURL_DISABLE_SHUFFLE_DNS=ON',
			'-DCURL_DISABLE_SMB=ON',
			'-DCURL_DISABLE_SMTP=ON',
			'-DCURL_DISABLE_TELNET=ON',
			'-DCURL_DISABLE_TFTP=ON',
			'-DCURL_USE_MBEDTLS=ON',
			'-DCURL_USE_LIBPSL=OFF',
			'-DCURL_USE_LIBSSH=OFF',
			'-DCURL_USE_LIBSSH2=OFF',
			'-DUSE_LIBIDN2=OFF',
			'-DUSE_NGHTTP2=OFF',
			'-DUSE_MANUAL=OFF'
		])

@target
class OpenEXR(Target):
	DEPS = [ 'llvm', 'cmake', 'ninja' ]
	def configure(self: Self, config: String, build: Build):
		build.cmake_configure(config, [
			'-DOPENEXR_INSTALL_TOOLS=OFF',
			'-DOPENEXR_BUILD_EXAMPLES=OFF',
			'-DOPENEXR_FORCE_INTERNAL_DEFLATE=ON'
		])
	def compile(self: Self, config: String, build: Build):
		build.cmake_compile(config)
	def install(self: Self, config: String, build: Build):
		build.cmake_install(config)

@target
class FreeType(Target):
	DEPS = [ 'llvm', 'cmake', 'ninja', 'zlib' ]
	def configure(self: Self, config: String, build: Build):
		build.cmake_configure(config, [
			'-DFT_REQUIRE_ZLIB=ON',
			'-DFT_DISABLE_BZIP2=ON',
			'-DFT_DISABLE_PNG=ON',
			'-DFT_DISABLE_HARFBUZZ=ON',
			'-DFT_DISABLE_BROTLI=ON'
		])

@target
class LibXML2(Target):
	DEPS = [ 'llvm', 'cmake', 'ninja', 'zlib' ]
	def configure(self: Self, config: String, build: Build):
		build.cmake_configure(config, [
			'-DLIBXML2_WITH_C14N=OFF',
			'-DLIBXML2_WITH_DEBUG=OFF',
			'-DLIBXML2_WITH_FTP=OFF',
			'-DLIBXML2_WITH_HTML=OFF',
			'-DLIBXML2_WITH_HTTP=OFF',
			'-DLIBXML2_WITH_LZMA=OFF',
			'-DLIBXML2_WITH_PROGRAMS=OFF',
			'-DLIBXML2_WITH_PYTHON=OFF',
			'-DLIBXML2_WITH_TESTS=OFF',
			'-DLIBXML2_WITH_ZLIB=ON',
			'-DLIBXML2_WITH_ICONV=OFF',
			'-DLIBXML2_WITH_LEGACY=ON'
		])

@target
class FBXSDK(Target):
	DEPS = [ 'zlib', 'libxml2' ]
	def configure(self: Self, config: String, build: Build):
		pass
	def compile(self: Self, config: String, build: Build):
		pass
	def install(self: Self, config: String, build: Build):
		build.cptree('include', os.path.join(build.prefix, 'include'))
		if platform.system() == 'Linux':
			build.cptree('lin', build.prefix)
		elif platform.system() == 'Darwin':
			build.cptree('mac', build.prefix)
		elif platform.system() == 'Windows':
			build.cptree('win', build.prefix)

@target
class PortMidi(Target):
	DEPS = [ 'llvm', 'cmake', 'ninja' ]

@target
class SDL2(Target):
	DEPS = [ 'llvm', 'cmake', 'ninja' ]
	def configure(self: Self, config: String, build: Build):
		build.cmake_configure(config, [
			'-DSDL2_DISABLE_SDL2MAIN=ON',
			'-DSDL2_DISABLE_UNINSTALL=ON',
			'-DSDL_MMX=OFF',
			'-DSDL_3DNOW=OFF',
			'-DSDL_ALTIVEC=OFF',
			'-DSDL_DISKAUDIO=OFF',
			'-DSDL_DUMMYAUDIO=OFF',
			'-DSDL_DIRECTFB=OFF',
			'-DSDL_DIRECTFB_SHARED=OFF',
			'-DSDL_DUMMYVIDEO=OFF',
			'-DSDL_OPENGLES=OFF',
			'-DSDL_PTHREADS_SEM=OFF',
			'-DSDL_OSS=OFF',
			'-DSDL_ALSA=OFF',
			'-DSDL_ALSA_SHARED=OFF',
			'-DSDL_JACK=OFF',
			'-DSDL_JACK_SHARED=OFF',
			'-DSDL_ESD=OFF',
			'-DSDL_ESD_SHARED=OFF',
			'-DSDL_PIPEWIRE=OFF',
			'-DSDL_PIPEWIRE_SHARED=OFF',
			'-DSDL_PULSEAUDIO=OFF',
			'-DSDL_PULSEAUDIO_SHARED=OFF',
			'-DSDL_ARTS=OFF',
			'-DSDL_ARTS_SHARED=OFF',
			'-DSDL_NAS=OFF',
			'-DSDL_NAS_SHARED=OFF',
			'-DSDL_SNDIO=OFF',
			'-DSDL_SNDIO_SHARED=OFF',
			'-DSDL_FUSIONSOUND=OFF',
			'-DSDL_FUSIONSOUND_SHARED=OFF',
			'-DSDL_LIBSAMPLERATE=OFF',
			'-DSDL_LIBSAMPLERATE_SHARED=OFF',
			'-DSDL_X11_SHARED=ON',
			'-DSDL_WAYLAND_SHARED=ON',
			'-DSDL_WAYLAND_LIBDECOR_SHARED=ON',
			'-DSDL_WAYLAND_QT_TOUCH=OFF',
			'-DSDL_RPI=OFF',
			'-DSDL_KMSDRM=OFF',
			'-DSDL_HIDAPI=OFF',
			'-DSDL_HIDAPI_LIBUSB=OFF',
			'-DSDL_HIDAPI_JOYSTICK=OFF',
			'-DSDL_VIRTUAL_JOYSTICK=OFF',
			'-DSDL_SHARED=OFF',
			'-DSDL_STATIC=ON',
			'-DSDL_TEST=OFF',
			'-DSDL_STATIC_PIC=ON',
			'-DSDL_TESTS=OFF',
			'-DSDL_AUDIO=OFF',
			'-DSDL_JOYSTICK=OFF',
			'-DSDL_MISC=OFF',
			'-DSDL_AUDIO=OFF',
			'-DSDL_FILESYSTEM=OFF',
			'-DSDL_HAPTIC=OFF',
			'-DSDL_HIDAPI=OFF',
			'-DSDL_JOYSTICK=OFF',
			'-DSDL_LOCALE=OFF',
			'-DSDL_OPENGLES=OFF'
		])

	def install(self: Self, config: String, build: Build):
		build.cmake_install(config)
		if platform.system() == 'Windows':
			# Rename SDL2-static.lib to SDL2.lib
			src = os.path.join(build.prefix, 'lib', 'SDL2-static.lib')
			dst = os.path.join(build.prefix, 'lib', 'SDL2.lib')
			build.mv(src, dst)

@target
class CBlosc(Target):
	DEPS = [ 'llvm', 'cmake', 'ninja', 'zlib' ]
	NAME = 'c-blosc'
	def configure(self: Self, config: String, build: Build):
		build.cmake_configure(config, [
			'-DCMAKE_POLICY_VERSION_MINIMUM=3.5',
			'-DBUILD_SHARED=OFF',
			'-DBUILD_TESTS=OFF',
			'-DBUILD_FUZZERS=OFF',
			'-DBUILD_BENCHMARKS=OFF',
			'-DPREFER_EXTERNAL_ZLIB=ON'
		])

@target
class ENet(Target):
	DEPS = [ 'llvm', 'cmake', 'ninja' ]
	def install(self: Self, config: String, build: Build):
		build.cmake_install(config)
		# ENet has a non-standard CMake as well where it puts static builds into an
		# unnecessary static directory. We will just move them where they belong and
		# remove that directory.
		dst_path = os.path.join(build.prefix, 'lib')
		src_path = os.path.join(dst_path, 'static')
		build.mvtree(src_path, dst_path)
		build.rmdir(src_path)

@target
class CGLTF(Target):
	DEPS = [ 'llvm', 'cmake', 'ninja' ]

@target
class Odin(Target):
	DEPS = [ 'llvm' ]
	PATH = os.path.join('..', 'Odin')

@target
class JLS(Target):
	DATE = False
	DEPS = [ 'llvm', 'enet' ]
	PATH = os.path.join('..', 'jls')

	def config(self: Self, config: String) -> String:
		return 'debug' if config == 'debug' else 'release'

	def configure(self: Self, config: String, build: Build):
		args = [sys.executable, 'configure.py']
		if config != 'release':
			args.append('debug')
		build.run(args)

	def compile(self: Self, config: String, build: Build):
		build.run([os.path.join(build.prefix, 'bin', 'ninja')])

	def install(self: Self, config: String, build: Build):
		build.cp(os.path.join(f'.build', build.toolchain.libname('jls')),
		         os.path.join(build.prefix, 'lib', build.toolchain.libname('jls')))

@target
class FBX(Target):
	DEPS = [ 'fbxsdk' ]
	PATH = os.path.join('..', 'jam', 'fbx')

# Each Product of ours inherits from this base class.
class Product(Target):
	DATE = False
	DEPS = [
		'stb-image',
		'stb-image-write',
		'zlib',
		'mbedtls',
		'curl',
		'openexr',
		'freetype',
		'libxml2',
		'fbxsdk',
		'portmidi',
		'sdl2',
		'c-blosc',
		'cgltf',
		'jls',
		'fbx'
	]
	def config(self: Self, config: String):
		return config
	def configure(self: Self, config: String, build: Build):
		# Nothing to configure for our products.
		pass
	def compile(self: Self, config: String, build: Build):
		# When compiling shipping builds we need to create programs.zip files which
		# are embedded into the executable. We used to use a tool called jri_embed
		# for this but it's superior to do it from this build script instead. Also.
		# remove them after compilation so that they do not leave a mess in the tree
		PROGRAMS_PATHS = [ os.path.join('..', 'jri'), os.path.join('..', 'jrf'), '.' ]
		try:
			if not Build.is_dev(config) and self.name != 'embergen': # Does not use JRI
				for path in PROGRAMS_PATHS:
					base = os.path.join(path, 'programs')
					shutil.make_archive(base, 'zip', base)
			return build.odin_compile(config)
		finally:
			for path in PROGRAMS_PATHS:
				build.rm(os.path.join(path, 'programs.zip'))

	def install(self: Self, config: String, build: Build):
		# On macos build app bundle.
		if not Build.is_dev(config) and platform.system() == 'Darwin':
			build.macos_package(type(self).__name__, self.name)
	def check(self: Self, config: String, build: Build):
		return build.odin_check(config)

@target
class EmberGen2(Product):
	DEPS = [ 'odin', *Product.DEPS ]
	PATH = os.path.join('..', 'embergen3')

@target
class EmptyGen(Product):
	DEPS = [ 'odin', *Product.DEPS ]
	PATH = os.path.join('..', 'emptygen')

@target
class GeoGen(Product):
	DEPS = [ 'odin', *Product.DEPS ]
	PATH = os.path.join('..', 'geogen')

@target
class IlluGen(Product):
	DEPS = [ 'odin', *Product.DEPS ]
	PATH = os.path.join('..', 'illugen')

@target
class LiquiGen(Product):
	DEPS = [ 'odin', *Product.DEPS ]
	PATH = os.path.join('..', 'liquigen')

if __name__ == '__main__':
	try:
		# Expect this to always run with a CWD where the script is.
		os.chdir(sys.path[0])
		TARGETS = [
			CMake, Ninja, LLVM, STBImage, STBImageWrite, ZLib, MBedTLS,
			Curl, OpenEXR, FreeType, LibXML2, FBXSDK, PortMidi, SDL2,
			CBlosc, ENet, CGLTF, Odin, JLS, FBX,
			EmberGen2, EmptyGen, GeoGen, IlluGen, LiquiGen
		]
		with Build(TARGETS) as build:
			build.go(sys.argv)
		print('Done')
	except KeyboardInterrupt:
		print('Build cancelled')
	except Error as error:
		print(error)
		sys.exit(1)
	except BaseException as error:
		print(f'Unexpected error occured: {error}')
		print(f'\t{traceback.format_exc()}')
		print('The consistency of the build might be compromised. You should run "rebuild"')
		sys.exit(1)
	sys.exit(0)
