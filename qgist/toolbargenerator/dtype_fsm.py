# -*- coding: utf-8 -*-

"""

QGIST TOOLBARGENERATOR
QGIS Plugin for Generating Toolbars
https://github.com/qgist/toolbargenerator

    qgist/toolbargenerator/dtype_fsm.py: finite state machine

    Copyright (C) 2017-2019 QGIST project <info@qgist.org>

<LICENSE_BLOCK>
The contents of this file are subject to the GNU General Public License
Version 2 ("GPL" or "License"). You may not use this file except in
compliance with the License. You may obtain a copy of the License at
https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt
https://github.com/qgist/toolbargenerator/blob/master/LICENSE

Software distributed under the License is distributed on an "AS IS" basis,
WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for the
specific language governing rights and limitations under the License.
</LICENSE_BLOCK>

"""

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (External Dependencies)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from PyQt5.QtWidgets import (
    QMainWindow,
    )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .dtype_toolbar import dtype_toolbar_class
from ..config import config_class
from ..error import (
    QgistAttributeError,
    QgistTypeError,
    QgistValueError,
    )
from ..util import translate


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class dtype_fsm_class:

    def __init__(self, toolbar_list, mainwindow, config = None):

        if not isinstance(toolbar_list, list):
            raise QgistTypeError(translate('global', '"toolbar_list" must be a list. (dtype_fsm)'))
        if any([not isinstance(item, dict) for item in toolbar_list]):
            raise QgistTypeError(translate('global', 'Items in toolbar_list must be dicts. (dtype_fsm)'))
        if not isinstance(mainwindow, QMainWindow):
            raise QgistTypeError(translate('global', '"mainwindow" must be a QGis mainwindow. (dtype_fsm)'))
        if not isinstance(config, config_class) and config is not None:
            raise QgistTypeError(translate('global', '"config" must be a "config_class" object or None. (dtype_fsm)'))

        self._config = config

        self._toolbar_dict = {
            item['name_internal']: dtype_toolbar_class(mainwindow = mainwindow, **item)
            for item in toolbar_list
            }
        self.keys = self._toolbar_dict.keys

    def __getitem__(self, name):

        if not isinstance(name, str):
            raise QgistTypeError(translate('global', '"name" must be str. (dtype_fsm item)'))
        if name not in self._toolbar_dict.keys():
            raise QgistValueError(translate('global', '"name" is not a known toolbar. (dtype_fsm item)'))

        return self._toolbar_dict[name]

    def __len__(self):

        return len(self._toolbar_dict)

    def new_toolbar(self, name, mainwindow):

        if not isinstance(name, str):
            raise QgistTypeError(translate('global', '"name" must be str. (dtype_fsm new)'))
        if not isinstance(mainwindow, QMainWindow):
            raise QgistTypeError(translate('global', '"mainwindow" must be a QGis mainwindow. (dtype_fsm new)'))

        if name in self._toolbar_dict.keys():
            raise QgistWorkbenchNameError(translate('global', '"name" is a known toolbar, i.e. already exists. (dtype_fsm new)'))
        if len(name) == 0:
            raise QgistWorkbenchNameError(translate('global', '"name" is empty. (dtype_fsm new)'))

        # TODO

        self._update_config()

    def delete_toolbar(self, name, mainwindow):

        if not isinstance(name, str):
            raise QgistTypeError(translate('global', '"name" must be str. (dtype_fsm delete)'))
        if not isinstance(mainwindow, QMainWindow):
            raise QgistTypeError(translate('global', '"mainwindow" must be a QGIS mainwindow. (dtype_fsm delete)'))

        if name not in self._toolbar_dict.keys():
            raise QgistValueError(translate('global', '"name" is not a known toolbar. (dtype_fsm delete)'))

        # TODO

        self._update_config()

    def rename_toolbar(self, old_name, new_name, mainwindow):

        if not isinstance(old_name, str):
            raise QgistTypeError(translate('global', '"old_name" must be str. (dtype_fsm rename)'))
        if not isinstance(new_name, str):
            raise QgistTypeError(translate('global', '"new_name" must be str. (dtype_fsm rename)'))
        if not isinstance(mainwindow, QMainWindow):
            raise QgistTypeError(translate('global', '"mainwindow" must be a QGis mainwindow. (dtype_fsm rename)'))
        if old_name not in self._toolbar_dict.keys():
            raise QgistValueError(translate('global', '"old_name" is not a known toolbar. (dtype_fsm rename)'))
        if new_name in self._toolbar_dict.keys():
            raise QgistValueError(translate('global', '"new_name" is a known toolbar, i.e. already exists. (dtype_fsm rename)'))
        if len(new_name) == 0:
            raise QgistValueError(translate('global', '"new_name" is empty. (dtype_fsm rename)'))
        if old_name == new_name:
            return

        # TODO

        self._update_config()

    def save_toolbar(self, name, mainwindow):

        if not isinstance(name, str):
            raise QgistTypeError(translate('global', '"name" must be str. (dtype_fsm save)'))
        if not isinstance(mainwindow, QMainWindow):
            raise QgistTypeError(translate('global', '"mainwindow" must be a QGis mainwindow. (dtype_fsm save)'))

        # TODO

        self._update_config()

    def as_list(self):

        return [item.as_dict() for item in self._toolbar_dict.values()]

    def _update_config(self):

        if self._config is None:
            return

        self._config['toolbar_list'] = self.as_list()
