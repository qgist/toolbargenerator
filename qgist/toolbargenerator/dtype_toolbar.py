# -*- coding: utf-8 -*-

"""

QGIST TOOLBARGENERATOR
QGIS Plugin for Generating Toolbars
https://github.com/qgist/toolbargenerator

    qgist/toolbargenerator/dtype_toolbar.py: toolbar datatype

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
# IMPORT (Python Standard Library)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import re


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (QGIS)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from qgis._gui import QgisInterface


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .const import SEPARATOR
from .dtype_action import (
    dtype_action_class,
    dtype_separator_class,
    )
from ..error import (
    QgistAttributeError,
    QgistTypeError,
    QgistValueError,
    )
from ..util import translate


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class dtype_toolbar_class:

    def __init__(self, name_internal, name_translated, actions_list, enabled, iface):

        if not isinstance(name_internal, str):
            raise QgistTypeError(translate('global', '"name_internal" must be str. (dtype_toolbar)'))
        if len(name_internal) == 0:
            raise QgistValueError(translate('global', '"name_internal" must not be empty. (dtype_toolbar)'))
        if not isinstance(name_translated, str):
            raise QgistTypeError(translate('global', '"name_translated" must be str. (dtype_toolbar)'))
        if len(name_translated) == 0:
            raise QgistValueError(translate('global', '"name_translated" must not be empty. (dtype_toolbar)'))
        if not isinstance(actions_list, list):
            raise QgistTypeError(translate('global', '"actions_list" must be a list. (dtype_toolbar)'))
        if not all([isinstance(item, dict) for item in actions_list]):
            raise QgistTypeError(translate('global', 'Items in "actions_list" must be dicts. (dtype_toolbar)'))
        if not isinstance(enabled, bool):
            raise QgistTypeError(translate('global', '"enabled" must be bool. (dtype_toolbar)'))
        if not isinstance(iface, QgisInterface):
            raise QgistTypeError(translate('global', '"iface" must be a QgisInterface object. (dtype_toolbar)'))

        self._name_internal = name_internal
        self._name_translated = name_translated
        self._actions_list = [dtype_action_class.from_dict(item) for item in actions_list]
        self._enabled = enabled

        self._loaded = False
        self._toolbar = None
        if self._enabled:
            self.load(iface)

    def load(self, iface):

        if not isinstance(iface, QgisInterface):
            raise QgistTypeError(translate('global', '"iface" must be a QgisInterface object. (dtype_toolbar load)'))

        if self._loaded:
            return

        self._toolbar = iface.addToolBar(self._name_translated)
        self._toolbar.setObjectName(self._name_internal)
        self._toolbar_fill(iface)

        self._loaded = True

    def reload(self, iface):

        if not isinstance(iface, QgisInterface):
            raise QgistTypeError(translate('global', '"iface" must be a QgisInterface object. (dtype_toolbar reload)'))

        if not self._loaded:
            return

        self._toolbar_clear()
        self._toolbar_fill(iface)

    def unload(self, iface):

        if not isinstance(iface, QgisInterface):
            raise QgistTypeError(translate('global', '"iface" must be a QgisInterface object. (dtype_toolbar unload)'))

        if not self._loaded:
            return

        self._toolbar_clear()
        iface.mainWindow().removeToolBar(self._toolbar) # fixes #4
        del self._toolbar # explicit ...
        self._toolbar = None

        self._loaded = False

    def rename(self, new_name_internal, new_name_translated, iface):

        if not isinstance(new_name_internal, str):
            raise QgistTypeError(translate('global', '"new_name_internal" must be str. (dtype_toolbar rename)'))
        if len(new_name_internal) == 0:
            raise QgistValueError(translate('global', '"new_name_internal" must not be empty. (dtype_toolbar rename)'))
        if not isinstance(new_name_translated, str):
            raise QgistTypeError(translate('global', '"new_name_translated" must be str. (dtype_toolbar rename)'))
        if len(new_name_translated) == 0:
            raise QgistValueError(translate('global', '"new_name_translated" must not be empty. (dtype_toolbar rename)'))
        if not isinstance(iface, QgisInterface):
            raise QgistTypeError(translate('global', '"iface" must be a QgisInterface object. (dtype_toolbar rename)'))

        self._name_internal = new_name_internal
        self._name_translated = new_name_translated

        if not self._enabled:
            return

        # self.reload will not reset toolbar name and object name - a new toolbar is required
        self.unload(iface)
        self.load(iface)

    def get_actions(self):

        return (
            action for action in self._actions_list
            )

    def update_actions(self, action_id_list, iface):

        if not isinstance(action_id_list, list):
            raise QgistTypeError(translate('global', '"action_id_list" must be a list. (dtype_toolbar update_actions)'))
        if not all([isinstance(action_id, str) for action_id in action_id_list]):
            raise QgistTypeError(translate('global', 'Items in "action_id_list" must be str. (dtype_toolbar update_actions)'))
        if not isinstance(iface, QgisInterface):
            raise QgistTypeError(translate('global', '"iface" must be a QgisInterface object. (dtype_toolbar update_actions)'))

        all_actions_dict = dtype_action_class.all_named_from_mainwindow_as_dict(iface.mainWindow())

        if not all([(action_id in all_actions_dict.keys()) for action_id in action_id_list]):
            raise QgistTypeError(translate('global', '"action_id_list" contains unknown action ids. (dtype_toolbar update_actions)'))

        for action in self._actions_list:
            action.disconnect()
        self._actions_list.clear()

        self._actions_list.extend([all_actions_dict[action_id] for action_id in action_id_list])

        if self._loaded:
            self.reload(iface)

    def _toolbar_clear(self):

        for action in self._actions_list:
            action.disconnect()

        self._toolbar.clear()

    def _toolbar_fill(self, iface):

        dtype_action_class.find_in_list(self._actions_list, iface.mainWindow())

        for action in self._actions_list:
            action.add_to_toolbar(self._toolbar)

    def as_dict(self):

        return dict(
            name_internal = self._name_internal,
            name_translated = self._name_translated,
            actions_list = [item.as_dict() for item in self._actions_list],
            enabled = self._enabled,
            )

    @property
    def name_internal(self):

        return self._name_internal

    @name_internal.setter
    def name_internal(self, value):

        raise QgistAttributeError(translate('global', '"name_internal" must not be changed. (dtype_toolbar name_internal)'))

    @property
    def name_translated(self):

        return self._name_translated

    @name_translated.setter
    def name_translated(self, value):

        raise QgistAttributeError(translate('global', '"name_translated" must not be changed. (dtype_toolbar name_translated)'))

    @staticmethod
    def translated_to_internal_name(name_translated):

        return translate('global', 'custom') + '_' + re.sub(r'\W+', '', name_translated)
