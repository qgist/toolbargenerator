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

from PyQt5.QtGui import (
    QIcon,
    )
from PyQt5.QtWidgets import (
    QFileDialog,
    QInputDialog,
    QListWidgetItem,
    )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .dtype_action import (
    dtype_action_class,
    dtype_separator_class,
    )
from .dtype_fsm import dtype_fsm_class
from .error import QgistToolbarNameError
from .ui_manager_base import ui_manager_base_class
from ..config import config_class
from ..error import (
    QgistConfigFormatError,
    Qgist_ALL_Errors,
    )
from ..msg import (
    msg_critical,
    msg_warning,
    )
from ..util import translate


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

        self._all_items_dict = {}

        all_actions_dict = dtype_action_class.all_named_from_mainwindow_as_dict(
            self._iface.mainWindow(), with_separator = False
            )
        for action_id in sorted(all_actions_dict.keys()):
            self._all_items_dict[action_id] = self._item_from_action(all_actions_dict[action_id])
            self._ui_dict['list_actions_all'].addItem(self._all_items_dict[action_id])
        self._ui_dict['list_actions_all'].setCurrentRow(0)

        self._ui_dict['text_filter'].textChanged.connect(self._text_filter_textchanged)

        for name in ('add', 'remove', 'up', 'down', 'new', 'delete', 'save', 'rename', 'import', 'export', 'separator'):
            self._ui_dict['toolbutton_%s' % name].clicked.connect(
                getattr(self, '_toolbutton_%s_clicked' % name)
                )
        self._ui_dict['list_toolbars'].currentRowChanged.connect(self._list_toolbars_currentrowchanged)

        self._update_view()

    def _item_from_action(self, action):

        item = QListWidgetItem(action.id)
        if action.action is not None:
            item.setIcon(action.action.icon())

        return item

    def _item_from_item(self, old_item):

        new_item = QListWidgetItem(old_item.text())
        new_item.setIcon(old_item.icon())

        return new_item

    def _text_filter_textchanged(self, new_text):

        new_text = str(new_text).lower()

        for id, item in self._all_items_dict.items():
            if new_text in id.lower():
                item.setHidden(False)
            else:
                item.setHidden(True)

    def _toolbutton_add_clicked(self):

        item = self._ui_dict['list_actions_all'].currentItem()
        if item is None:
            return
        self._ui_dict['list_actions_toolbar'].addItem(self._item_from_item(item))

    def _toolbutton_remove_clicked(self):

        self._ui_dict['list_actions_toolbar'].takeItem(
            self._ui_dict['list_actions_toolbar'].currentRow()
            )

    def _toolbutton_up_clicked(self):

        index = int(self._ui_dict['list_actions_toolbar'].currentRow())
        if index <= 0:
            return
        item = self._ui_dict['list_actions_toolbar'].takeItem(index)
        self._ui_dict['list_actions_toolbar'].insertItem(index - 1, item)
        self._ui_dict['list_actions_toolbar'].setCurrentRow(index - 1)

    def _toolbutton_down_clicked(self):

        index = int(self._ui_dict['list_actions_toolbar'].currentRow())
        if index >= self._ui_dict['list_actions_toolbar'].count():
            return
        item = self._ui_dict['list_actions_toolbar'].takeItem(index)
        self._ui_dict['list_actions_toolbar'].insertItem(index + 1, item)
        self._ui_dict['list_actions_toolbar'].setCurrentRow(index + 1)

    def _toolbutton_new_clicked(self):

        new_name_translated, user_ok = QInputDialog.getText(
            self,
            translate('global', 'New toolbar'),
            translate('global', 'Name of new toolbar')
            )

        if not user_ok:
            return

        try:
            self._fsm.new_toolbar(new_name_translated, self._iface)
            self._update_view()
            self._select_toolbar(new_name_translated)
        except QgistToolbarNameError as e:
            msg_warning(e, self)
            return
        except Qgist_ALL_Errors as e:
            msg_critical(e, self)
            self.reject()
            return

    def _toolbutton_delete_clicked(self):

        current_item = self._ui_dict['list_toolbars'].currentItem()
        if current_item is None:
            return
        name_translated = str(current_item.text())

        try:
            self._fsm.delete_toolbar(name_translated, self._iface)
            self._update_view()
        except Qgist_ALL_Errors as e:
            msg_critical(e, self)
            self.reject()
            return

    def _toolbutton_save_clicked(self):

        current_item = self._ui_dict['list_toolbars'].currentItem()
        if current_item is None:
            return
        name_translated = str(current_item.text())

        try:
            self._fsm.save_toolbar(name_translated, self._iface, self._get_selected_actions())
            self._update_view()
            self._select_toolbar(name_translated)
        except Qgist_ALL_Errors as e:
            msg_critical(e, self)
            self.reject()
            return

    def _toolbutton_rename_clicked(self):

        current_item = self._ui_dict['list_toolbars'].currentItem()
        if current_item is None:
            return
        old_name_translated = str(current_item.text())

        new_name_translated, user_ok = QInputDialog.getText(
            self,
            translate('global', 'Rename toolbar'),
            translate('global', 'New name for toolbar')
            )

        if not user_ok:
            return

        try:
            self._fsm.rename_toolbar(old_name_translated, new_name_translated, self._iface)
            self._update_view()
            self._select_toolbar(new_name_translated)
        except QgistToolbarNameError as e:
            msg_warning(e, self)
            return
        except Qgist_ALL_Errors as e:
            msg_critical(e, self)
            self.reject()
            return

    def _toolbutton_import_clicked(self):

        fn, user_ok = QFileDialog.getOpenFileName(
            self,
            translate('global', 'Import toolbar from file'),
            '',
            'JSON files (*.json);;All Files (*)',
            options = QFileDialog.Options(),
            )
        if not user_ok:
            return

        try:
            self._fsm.import_toolbar(config_class.import_config(fn), self._iface)
            self._update_view()
        except (QgistToolbarNameError, QgistConfigFormatError) as e:
            msg_warning(e, self)
            return
        except Qgist_ALL_Errors as e:
            msg_critical(e, self)
            self.reject()
            return

    def _toolbutton_export_clicked(self):

        current_item = self._ui_dict['list_toolbars'].currentItem()
        if current_item is None:
            return
        name_translated = str(current_item.text())

        fn, user_ok = QFileDialog.getSaveFileName(
            self,
            translate('global', 'Export toolbar to file'),
            '',
            'JSON files (*.json);;All Files (*)',
            options = QFileDialog.Options(),
            )
        if not user_ok:
            return

        try:
            config_class.export_config(fn, self._fsm.export_toolbar(name_translated))
        except Qgist_ALL_Errors as e:
            msg_critical(e, self)
            self.reject()
            return

    def _toolbutton_separator_clicked(self):

        self._ui_dict['list_actions_toolbar'].addItem(
            QListWidgetItem(self._item_from_action(dtype_separator_class()))
            )

    def _get_selected_actions(self):

        return [
            str(self._ui_dict['list_actions_toolbar'].item(index).text())
            for index in range(self._ui_dict['list_actions_toolbar'].count())
            ]

    def _list_toolbars_currentrowchanged(self):

        self._ui_dict['list_actions_toolbar'].clear()

        current_item = self._ui_dict['list_toolbars'].currentItem()
        if current_item is None:
            return
        name_translated = str(current_item.text())

        for action in self._fsm[name_translated].get_actions():
            self._ui_dict['list_actions_toolbar'].addItem(self._item_from_action(action))

    def _select_toolbar(self, name_translated):

        index = list(sorted(self._fsm.keys())).index(name_translated)
        self._ui_dict['list_toolbars'].setCurrentRow(index)

    def _update_view(self):

        self._ui_dict['list_toolbars'].clear()
        self._ui_dict['list_actions_toolbar'].clear()

        for name_internal in sorted(self._fsm.keys()):
            self._ui_dict['list_toolbars'].addItem(
                QListWidgetItem(self._fsm[name_internal].name_translated)
                )
