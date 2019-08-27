# -*- coding: utf-8 -*-

"""

QGIST TOOLBARGENERATOR
QGIS Plugin for Generating Toolbars
https://github.com/qgist/toolbargenerator

    qgist/toolbargenerator/ui_manager.py: toolbargenerator manager ui class

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

import os


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (QGIS)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from qgis._gui import QgisInterface


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (External Dependencies)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# from PyQt5.QtCore import (
#     Qt,
#     )
from PyQt5.QtGui import (
    QIcon,
    )
from PyQt5.QtWidgets import (
    QListWidgetItem,
    )

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .dtype_fsm import dtype_fsm_class
from .ui_manager_base import ui_manager_base_class


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class ui_manager_class(ui_manager_base_class):

    def __init__(self, plugin_root_fld, iface, fsm):

        if not isinstance(plugin_root_fld, str):
            raise QgistTypeError(translate('global', '"plugin_root_fld" must be str. (ui_manager)'))
        if not os.path.exists(plugin_root_fld):
            raise QgistValueError(translate('global', '"plugin_root_fld" must exists. (ui_manager)'))
        if not os.path.isdir(plugin_root_fld):
            raise QgistValueError(translate('global', '"plugin_root_fld" must be a directory. (ui_manager)'))
        if not isinstance(iface, QgisInterface):
            raise QgistTypeError(translate('global', '"iface" must be a QgisInterface. (ui_manager)'))
        if not isinstance(fsm, dtype_fsm_class):
            raise QgistTypeError(translate('global', '"fsm" must be a toolbar generator finite state machine. (ui_manager)'))

        super().__init__(plugin_root_fld)

        self._plugin_root_fld = plugin_root_fld
        self._iface = iface
        self._fsm = fsm

        self._connect_ui()

    def _connect_ui(self):

        self._item_dict = {}

        for action_id in sorted(self._fsm.all_actions.keys()):
            self._item_dict[action_id] = self._item_from_action(self._fsm.all_actions[action_id])
            self._ui_dict['list_actions_all'].addItem(self._item_dict[action_id])
        self._ui_dict['list_actions_all'].setCurrentRow(0)

        self._ui_dict['text_filter'].textChanged.connect(self._text_filter_textchanged)
        self._ui_dict['toolbutton_add'].clicked.connect(self._toolbutton_add_clicked)

    def _item_from_action(self, action):

        item = QListWidgetItem(action.id)
        item.setIcon(action.action.icon())

        return item

    def _item_from_item(self, old_item):

        new_item = QListWidgetItem(old_item.text())
        new_item.setIcon(old_item.icon())

        return new_item

    def _text_filter_textchanged(self, new_text):

        new_text = str(new_text).lower()

        for id, item in self._item_dict.items():
            if new_text in id.lower():
                item.setHidden(False)
            else:
                item.setHidden(True)

    def _toolbutton_add_clicked(self):

        item = self._ui_dict['list_actions_all'].currentItem()
        if item is None:
            return
        self._ui_dict['list_actions_toolbar'].addItem(self._item_from_item(item))
