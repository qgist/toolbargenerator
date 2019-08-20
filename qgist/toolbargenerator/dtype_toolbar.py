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
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .dtype_action import dtype_action_class


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class dtype_toolbar_class:

    def __init__(self, iface, name_internal, name_translated, actions_list, enabled):

        self._name_internal = name_internal
        self._name_translated = name_translated
        self._actions_list = actions_list # TODO
        self._enabled = enabled

        self._loaded = False
        if self._enabled:
            self.load(iface)

    def load(self, iface):

        if self._loaded:
            return

        # TODO

        self._loaded = True

    def unload(self, iface):

        if not self._loaded:
            return

        # TODO

        self._loaded = False

    def as_dict(self):

        return dict(
            name_internal = self._name_internal,
            name_translated = self._name_translated,
            actions_list = None, # TODO
            enabled = self._enabled,
            )
