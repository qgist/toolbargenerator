# -*- coding: utf-8 -*-

"""

QGIST TOOLBARGENERATOR
QGIS Plugin for Generating Toolbars
https://github.com/qgist/toolbargenerator

    qgist/toolbargenerator/ui_manager_base.py: toolbargenerator manager ui base class

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
# IMPORT (External Dependencies)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from PyQt5.QtCore import (
    QSize,
    Qt,
    )
from PyQt5.QtGui import (
    QIcon,
    )
from PyQt5.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QSizePolicy,
    QSpacerItem,
    QToolButton,
    QVBoxLayout,
    )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from ..const import ICON_FLD
from ..util import translate


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class ui_manager_base_class(QDialog):

    def __init__(self, plugin_root_fld):

        super().__init__()

        self.setWindowTitle(translate('global', 'Toolbar Manager'))

        self._ui_dict = {
            'layout_0_v_root': QVBoxLayout(), # dialog
            'layout_1_h_lists': QHBoxLayout(), # three lists
            }
        self.setLayout(self._ui_dict['layout_0_v_root'])
        self._ui_dict['layout_0_v_root'].addLayout(self._ui_dict['layout_1_h_lists'])

        for position, name, title, items in (
            ('left', 'toolbars', translate('global', 'Toolbars'), (
                ('new', translate('global', 'New toolbar'), 'FileNew.svg'),
                ('delete', translate('global', 'Delete toolbar'), 'Delete.svg'),
                ('save', translate('global', 'Save toolbar'), 'Save.svg'),
                )),
            ('center', 'actions_toolbar', translate('global', 'Selected actions'), (
                ('up', translate('global', 'Move action up'), 'ActionUp.svg'),
                ('down', translate('global', 'Move action down'), 'ActionDown.svg'),
                ('remove', translate('global', 'Remove action'), 'ActionRemove.svg'),
                )),
            ('right', 'actions_all', translate('global', 'Available actions'), (
                ('add', translate('global', 'Add action'), 'ActionAdd.svg'),
                )),
            ):

            layout = 'layout_2_v_%s' % position
            layout_toolbar = 'layout_3_h_%s_toolbar' % position
            self._ui_dict[layout] = QVBoxLayout()
            self._ui_dict['layout_1_h_lists'].addLayout(self._ui_dict[layout])
            self._ui_dict[layout_toolbar] = QHBoxLayout()
            self._ui_dict[layout].addLayout(self._ui_dict[layout_toolbar])

            self._ui_dict['label_' + position] = QLabel(title)
            self._ui_dict[layout].addWidget(self._ui_dict['label_' + position])

            ui_manager_base_class._init_dialogtoolbar(
                self._ui_dict, self._ui_dict[layout_toolbar], plugin_root_fld, items
                )

            self._ui_dict['list_' + name] = QListWidget()
            self._ui_dict[layout].addWidget(self._ui_dict['list_' + name])

            if position == 'right':
                self._ui_dict['text_filter'] = QLineEdit()
                self._ui_dict['text_filter'].setSizePolicy(
                    QSizePolicy.Expanding, QSizePolicy.Fixed
                    )
                self._ui_dict[layout].addWidget(self._ui_dict['text_filter'])

    @staticmethod
    def _init_dialogtoolbar(ui_dict, toolbar_layout, plugin_root_fld, items):

        toolbar_layout.setSpacing(0)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)

        for name, title, icon in items:

            if name == None:
                toolbar_layout.addItem(QSpacerItem(10, 10))
                continue

            toolbutton = QToolButton()
            toolbutton.setToolTip(title)
            toolbutton.setIcon(QIcon(os.path.join(
                plugin_root_fld, ICON_FLD, icon
            )))
            toolbutton.setIconSize(QSize(24, 24))  # TODO get icon size from QGis!!!
            toolbutton.setAutoRaise(True)
            toolbutton.setFocusPolicy(Qt.NoFocus)

            ui_dict['toolbutton_{NAME:s}'.format(NAME = name)] = toolbutton

            toolbar_layout.addWidget(toolbutton)

        toolbar_layout.addStretch()
