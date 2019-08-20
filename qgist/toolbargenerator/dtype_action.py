# -*- coding: utf-8 -*-

"""

QGIST TOOLBARGENERATOR
QGIS Plugin for Generating Toolbars
https://github.com/qgist/toolbargenerator

    qgist/toolbargenerator/dtype_action.py: toolbar action

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
    QAction,
    QMainWindow,
    )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .error import (
    QgistActionConfusionError,
    QgistActionFound,
    QgistActionNotFoundError,
    QgistUnnamedActionError,
    )
from ..error import (
    QgistAttributeError,
    QgistTypeError,
    )
from ..util import translate


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class dtype_toolbar_action:

    def __init__(self, name_internal, name_translated, parent_name_internal):

        if not isinstance(name_internal, str):
            raise QgistTypeError(translate('global', '"name_internal" must be a str. (dtype_action)'))
        if not isinstance(name_translated, str):
            raise QgistTypeError(translate('global', '"name_translated" must be a str. (dtype_action)'))
        if not isinstance(parent_name_internal, str):
            raise QgistTypeError(translate('global', '"parent_name_internal" must be a str. (dtype_action)'))

        self._name_internal = name_internal
        self._name_translated = name_translated
        self._parent_name_internal = parent_name_internal

        self._present = False
        self._action = None

    def find(self, all_actions):

        def search_by(func, name):
            temp_dict = {func(action): action for action in all_actions}
            temp_names = [func(action) for action in all_actions]
            name_count = temp_names.count(name)
            if name_count != 1:
                self._action, self._present = None, False
                if name_count == 0:
                    raise QgistActionNotFoundError('"{NAME:s}": '.format(NAME = str(name)) + translate('global', 'Action could not be found. (dtype_action find)'))
                else:
                    raise QgistActionConfusionError('"{NAME:s}": '.format(NAME = str(name)) + translate('global', 'Confused, multiple matching actions. (dtype_action find)'))
            else:
                self._action, self._present = temp_dict[name], True
                raise QgistActionFound()

        if not isinstance(all_actions, list):
            raise QgistTypeError(translate('global', '"all_actions" must be a list. (dtype_action find)'))
        if not all([isinstance(item, dict) for item in all_actions]):
            raise QgistTypeError(translate('global', 'Items in "all_actions" must be dicts. (dtype_action find)'))

        if self._name_internal != '':
            try:
                search_by(
                    lambda item: item['name_internal'],
                    self._name_internal
                    )
            except QgistActionNotFoundError:
                pass
            except QgistActionFound:
                self._name_translated = str(self._action.text())
                return

        if self._name_translated == '':
            self._action, self._present = None, False
            raise QgistActionNotFoundError('"{NAME:s}": '.format(NAME = self._name_translated) + translate('global', 'Action could not be found. (dtype_action  find)'))

        try:
            search_by(
                lambda item: item['name_translated'],
                self._name_translated
                )
        except QgistActionNotFoundError:
            pass
        except QgistActionFound:
            return

        try:
            search_by(
                lambda item: (item['name_translated'], item['parent_name_internal']),
                self._name_translated, self._parent_name_internal
                )
        except QgistActionFound:
            return

    def disconnect(self):

        if not self._present:
            return

        self._action, self._present = None, False

    @property
    def action(self):

        return self._name_internal

    @action.setter
    def action(self, value):

        raise QgistAttributeError(translate('global', '"action" must not be changed. (dtype_action action)'))

    @property
    def name_internal(self):

        return self._name_internal

    @name_internal.setter
    def name_internal(self, value):

        raise QgistAttributeError(translate('global', '"name_internal" must not be changed. (dtype_action name_internal)'))

    @property
    def name_translated(self):

        return self._name_translated

    @name_translated.setter
    def name_translated(self, value):

        raise QgistAttributeError(translate('global', '"name_translated" must not be changed. (dtype_action name_translated)'))

    @property
    def parent_name_internal(self):

        return self._parent_name_internal

    @parent_name_internal.setter
    def parent_name_internal(self, value):

        raise QgistAttributeError(translate('global', '"parent_name_internal" must not be changed. (dtype_action parent_name_internal)'))

    def as_dict(self):

        return dict(
            name_internal = self._name_internal,
            name_translated = self._name_translated,
            parent_name_internal = self._parent_name_internal,
            )

    @staticmethod
    def _dict_from_action(action, include_action = False):

        action_dict = dict(
            name_internal = str(action.objectName()),
            name_translated = str(action.text()),
            parent_name_internal = str(action.parent().objectName()),
            )

        if action_dict['name_internal'] == '' and action_dict['name_translated'] == '':
            raise QgistUnnamedActionError(translate('global', '"name_internal" and "name_translated" are empty. (dtype_action _dict_from_action)'))

        if include_action:
            action_dict['action'] = action

        return action_dict

    @staticmethod
    def get_all_actions(mainwindow):

        if not isinstance(mainwindow, QMainWindow):
            raise QgistTypeError(translate('global', '"mainwindow" must be a QGis mainwindow. (dtype_action get_all_actions)'))

        return [
            dtype_toolbar_action._dict_from_action(action, include_action = True)
            for action in mainwindow.findChildren(QAction)
            ]

    @staticmethod
    def from_action(action):

        if not isinstance(action, QAction):
            raise QgistTypeError(translate('global', '"action" must be a QAction. (dtype_action from_action)'))

        return dtype_toolbar_action(
            **dtype_toolbar_action._dict_from_action(action)
            )
