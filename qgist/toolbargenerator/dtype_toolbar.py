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
# IMPORT (QGIS)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from qgis._gui import QgisInterface


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .error import (
    QgistActionConfusionError,
    QgistActionNotFoundError,
    )
from .dtype_action import dtype_action_class
from ..error import (
    QgistTypeError,
    QgistValueError,
    )
from ..msg import msg_warning
from ..util import translate


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class dtype_toolbar_class:

    def __init__(self, iface, name_internal, name_translated, actions_list, enabled, iface):

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
        self._actions_list = [dtype_action_class(**item) for item in actions_list]
        self._enabled = enabled

        self._loaded = False
        self._toolbar = None
        if self._enabled:
            self.load(iface)

    def load(self, iface):

        if not isinstance(iface, QgisInterface):
            raise QgistTypeError(translate('global', '"iface" must be a QgisInterface object. (dtype_toolbar)'))

        if self._loaded:
            return

        self._toolbar = iface.addToolBar(self._name_translated)
        self._toolbar.setObjectName(self._name_internal)
        self._toolbar_fill(iface)

        self._loaded = True

    def reload(self, iface):

        if not isinstance(iface, QgisInterface):
            raise QgistTypeError(translate('global', '"iface" must be a QgisInterface object. (dtype_toolbar)'))

        if not self._loaded:
            return

        self._toolbar_clear()
        self._toolbar_clear(iface)

    def unload(self, iface):

        if not isinstance(iface, QgisInterface):
            raise QgistTypeError(translate('global', '"iface" must be a QgisInterface object. (dtype_toolbar)'))

        if not self._loaded:
            return

        for action in self._actions_list:
            action.disconnect()

        del self._toolbar # explicit ...
        self._toolbar = None

        self._loaded = False

    def _toolbar_clear(self):

        self._toolbar.clear()

    def _toolbar_fill(self, iface):

        mainwindow = iface.mainWindow()
        all_actions = dtype_action_class.get_all_actions(mainwindow)
        for action in self._actions_list:
            try:
                action.find(all_actions)
                self._toolbar.addAction(action.action)
            except (QgistActionConfusionError, QgistActionNotFoundError) as e:
                msg_warning(e, mainwindow)

    def as_dict(self):

        return dict(
            name_internal = self._name_internal,
            name_translated = self._name_translated,
            actions_list = [item.as_dict() for item in self._actions_list],
            enabled = self._enabled,
            )
