"""
utils
"""
from __future__ import print_function
import sys
import shlex
import subprocess
import os
import io


DEBUG = bool(os.environ.get("SETUPTOOLS_SCM_DEBUG"))


def trace(*k):
    if DEBUG:
        print(*k)
        sys.stdout.flush()


def ensure_stripped_str(str_or_bytes):
    if isinstance(str_or_bytes, str):
        return str_or_bytes.strip()
    else:
        return str_or_bytes.decode('utf-8', 'surogate_escape').strip()


def do_ex(cmd, cwd='.'):
    trace('cmd', repr(cmd))
    p = subprocess.Popen(
        shlex.split(cmd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=cwd,
        env=dict(
            os.environ,
            # disable hgrc processing other than .hg/hgrc
            HGRCPATH='',
            # try to disable i18n
            LC_ALL='C',
            LANGUAGE='',
            HGPLAIN='1',
        )
    )

    out, err = p.communicate()
    if out:
        trace('out', repr(out))
    if err:
        trace('err', repr(err))
    if p.returncode:
        trace('ret', p.returncode)
    return ensure_stripped_str(out), ensure_stripped_str(err), p.returncode


def do(cmd, cwd='.'):
    out, err, ret = do_ex(cmd, cwd)
    if ret:
        trace('ret', ret)
        print(err)
    return out


def data_from_mime(path):
    with io.open(path, encoding='utf-8') as fp:
        content = fp.read()
    trace('content', repr(content))
    # the complex conditions come from reading pseudo-mime-messages
    data = dict(
        x.split(': ', 1)
        for x in content.splitlines()
        if ': ' in x)
    trace('data', data)
    return data
