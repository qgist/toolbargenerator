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
# IMPORT (QGIS)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from qgis._gui import QgisInterface


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .dtype_toolbar import dtype_toolbar_class
from .error import QgistToolbarNameError
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

    def __init__(self, toolbar_list, iface, config = None):

        if not isinstance(toolbar_list, list):
            raise QgistTypeError(translate('global', '"toolbar_list" must be a list. (dtype_fsm)'))
        if any([not isinstance(item, dict) for item in toolbar_list]):
            raise QgistTypeError(translate('global', 'Items in toolbar_list must be dicts. (dtype_fsm)'))
        if not isinstance(iface, QgisInterface):
            raise QgistTypeError(translate('global', '"iface" must be a QgisInterface. (dtype_fsm)'))
        if not isinstance(config, config_class) and config is not None:
            raise QgistTypeError(translate('global', '"config" must be a "config_class" object or None. (dtype_fsm)'))

        self._config = config

        self._toolbar_dict = {
            item['name_translated']: dtype_toolbar_class(iface = iface, **item)
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

    def new_toolbar(self, name_translated, iface):

        if not isinstance(name_translated, str):
            raise QgistTypeError(translate('global', '"name_translated" must be str. (dtype_fsm new)'))
        if not isinstance(iface, QgisInterface):
            raise QgistTypeError(translate('global', '"iface" must be a QgisInterface. (dtype_fsm new)'))

        if name_translated in self._toolbar_dict.keys():
            raise QgistToolbarNameError(translate('global', '"name_translated" is a known toolbar, i.e. already exists. (dtype_fsm new)'))
        if len(name_translated) == 0:
            raise QgistToolbarNameError(translate('global', '"name_translated" is empty. (dtype_fsm new)'))

        name_internal = dtype_toolbar_class.translated_to_internal_name(name_translated)
        if name_internal in {item.name_internal for item in self._toolbar_dict.values()}:
            raise QgistToolbarNameError(translate('global', '"name_translated" is translated to a known toolbar, i.e. already exists. (dtype_fsm new)'))

        self._toolbar_dict[name_translated] = dtype_toolbar_class(
            name_internal = name_internal,
            name_translated = name_translated,
            actions_list = [],
            enabled = True,
            iface = iface,
            )

        self._update_config()

    def delete_toolbar(self, name_translated, iface):

        if not isinstance(name_translated, str):
            raise QgistTypeError(translate('global', '"name_translated" must be str. (dtype_fsm delete)'))
        if not isinstance(iface, QgisInterface):
            raise QgistTypeError(translate('global', '"iface" must be a QgisInterface. (dtype_fsm delete)'))

        if name_translated not in self._toolbar_dict.keys():
            raise QgistValueError(translate('global', '"name_translated" is not a known toolbar. (dtype_fsm delete)'))

        deleted_toolbar = self._toolbar_dict.pop(name_translated)
        deleted_toolbar.unload(iface)

        self._update_config()

    def rename_toolbar(self, old_name_translated, new_name_translated, iface):

        if not isinstance(old_name_translated, str):
            raise QgistTypeError(translate('global', '"old_name_translated" must be str. (dtype_fsm rename)'))
        if not isinstance(new_name_translated, str):
            raise QgistTypeError(translate('global', '"new_name_translated" must be str. (dtype_fsm rename)'))
        if not isinstance(iface, QgisInterface):
            raise QgistTypeError(translate('global', '"iface" must be a QgisInterface. (dtype_fsm rename)'))
        if old_name_translated not in self._toolbar_dict.keys():
            raise QgistValueError(translate('global', '"old_name_translated" is not a known toolbar. (dtype_fsm rename)'))
        if new_name_translated in self._toolbar_dict.keys():
            raise QgistValueError(translate('global', '"new_name_translated" is a known toolbar, i.e. already exists. (dtype_fsm rename)'))
        if len(new_name_translated) == 0:
            raise QgistValueError(translate('global', '"new_name_translated" is empty. (dtype_fsm rename)'))
        if old_name_translated == new_name_translated:
            return

        internal_names = {item.name_internal for item in self._toolbar_dict.values()}

        old_name_internal = dtype_toolbar_class.translated_to_internal_name(old_name_translated)
        if old_name_internal not in internal_names:
            raise QgistToolbarNameError(translate('global', '"old_name_translated" is not translated to a known toolbar, i.e. does not exist. (dtype_fsm rename)'))

        new_name_internal = dtype_toolbar_class.translated_to_internal_name(new_name_translated)
        if new_name_internal in internal_names:
            raise QgistToolbarNameError(translate('global', '"new_name_translated" is translated to a known toolbar, i.e. already exists. (dtype_fsm rename)'))

        self._toolbar_dict[old_name_translated].rename(
            new_name_internal, new_name_translated, iface
            )
        self._toolbar_dict[new_name_translated] = self._toolbar_dict.pop(old_name_translated)

        self._update_config()

    def save_toolbar(self, name_translated, iface, name_list):

        if not isinstance(name_translated, str):
            raise QgistTypeError(translate('global', '"name_translated" must be str. (dtype_fsm save)'))
        if name_translated not in self._toolbar_dict.keys():
            raise QgistValueError(translate('global', '"name_translated" is not a known toolbar. (dtype_fsm save)'))
        if not isinstance(iface, QgisInterface):
            raise QgistTypeError(translate('global', '"iface" must be a QgisInterface. (dtype_fsm save)'))
        if not isinstance(name_list, list):
            raise QgistTypeError(translate('global', '"name_list" must be a list. (dtype_fsm save)'))
        if not all([isinstance(name, str) for name in name_list]):
            raise QgistTypeError(translate('global', 'Items in "name_list" must be str. (dtype_fsm save)'))

        self._toolbar_dict[name_translated].update_actions(name_list, iface)

        self._update_config()

    def import_toolbar(self, toolbar_dict, iface):

        if not isinstance(toolbar_dict, dict):
            raise QgistTypeError(translate('global', '"toolbar_dict" must be a dict. (dtype_fsm import)'))
        if 'name_translated' not in toolbar_dict.keys():
            raise QgistValueError(translate('global', '"toolbar_dict" does not contain a translated name. (dtype_fsm import)'))
        if not isinstance(iface, QgisInterface):
            raise QgistTypeError(translate('global', '"iface" must be a QgisInterface. (dtype_fsm import)'))

        name_translated = toolbar_dict['name_translated']

        if name_translated in self._toolbar_dict.keys():
            raise QgistWorkbenchNameError(translate('global', '"name_translated" is a known toolbar, i.e. already exists. (dtype_fsm import)'))
        if len(name_translated) == 0:
            raise QgistWorkbenchNameError(translate('global', '"name_translated" is empty. (dtype_fsm import)'))

        self._toolbar_dict[name_translated] = dtype_toolbar_class(iface = iface, **toolbar_dict)

        self._update_config()

    def export_toolbar(self, name_translated):

        if not isinstance(name_translated, str):
            raise QgistTypeError(translate('global', '"name_translated" must be str. (dtype_fsm export)'))
        if name_translated not in self._toolbar_dict.keys():
            raise QgistValueError(translate('global', '"name_translated" is not a known toolbar. (dtype_fsm export)'))

        return self._toolbar_dict[name_translated].as_dict()

    def as_list(self):

        return [item.as_dict() for item in self._toolbar_dict.values()]

    def _update_config(self):

        if self._config is None:
            return

        self._config['toolbar_list'] = self.as_list()
