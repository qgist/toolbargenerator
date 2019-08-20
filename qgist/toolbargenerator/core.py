# -*- coding: utf-8 -*-

"""

QGIST TOOLBARGENERATOR
QGIS Plugin for Generating Toolbars
https://github.com/qgist/toolbargenerator

    qgist/toolbargenerator/core.py: QGIST toolbargenerator core

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
import platform


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (External Dependencies)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from PyQt5.QtGui import (
    QIcon,
    )
from PyQt5.QtWidgets import (
    QAction,
    )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .dtype_fsm import dtype_fsm_class
from .ui_manager import ui_manager_class
from ..config import (
    config_class,
    get_config_path,
    )
from ..const import (
    ICON_FLD,
    TRANSLATION_FLD,
    )
from ..error import (
    Qgist_ALL_Errors,
    QgistTypeError,
    QgistValueError,
    )
from ..msg import msg_critical
from ..util import (
    translate,
    setupTranslation,
    )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS: TOOLBARGENERATOR CORE
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class toolbargenerator:

    def __init__(self, iface, plugin_root_fld):

        if not hasattr(iface, 'mainWindow'):
            raise QgistTypeError(translate('global', '"iface" must be a QGIS iface object. (toolbargenerator)'))
        if not isinstance(plugin_root_fld, str):
            raise QgistTypeError(translate('global', '"plugin_root_fld" must be str. (toolbargenerator)'))
        if not os.path.exists(plugin_root_fld):
            raise QgistValueError(translate('global', '"plugin_root_fld" must exists. (toolbargenerator)'))
        if not os.path.isdir(plugin_root_fld):
            raise QgistValueError(translate('global', '"plugin_root_fld" must be a directory. (toolbargenerator)'))

        self._iface = iface
        self._plugin_root_fld = plugin_root_fld

        self._mainwindow = self._iface.mainWindow()
        self._system = platform.system()
