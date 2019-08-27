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
    )
from ..error import (
    QgistAttributeError,
    QgistTypeError,
    )
from ..msg import msg_warning
from ..util import translate


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class dtype_action_class:

    def __init__(self, name_internal, name_translated, parent_name_internal, action = None):

        if not isinstance(name_internal, str):
            raise QgistTypeError(translate('global', '"name_internal" must be a str. (dtype_action)'))
        if not isinstance(name_translated, str):
            raise QgistTypeError(translate('global', '"name_translated" must be a str. (dtype_action)'))
        if not isinstance(parent_name_internal, str):
            raise QgistTypeError(translate('global', '"parent_name_internal" must be a str. (dtype_action)'))
        if not isinstance(action, QAction) and action is not None:
            raise QgistTypeError(translate('global', '"action" must be a QAction or None. (dtype_action)'))

        self._name_internal = name_internal
        self._name_translated = name_translated
        self._parent_name_internal = parent_name_internal

        if action is None:
            self._present = False
            self._action = None
        else:
            self._present = True
            self._action = action

        self._create_id()

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
        if not all([isinstance(item, dtype_action_class) for item in all_actions]):
            raise QgistTypeError(translate('global', 'Items in "all_actions" must be of type dtype_action_class. (dtype_action find)'))

        if self._name_internal != '':
            try:
                search_by(
                    lambda item: getattr(item, 'name_internal'),
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
                lambda item: getitem(item, 'name_translated'),
                self._name_translated
                )
        except QgistActionNotFoundError:
            pass
        except QgistActionFound:
            return

        try:
            search_by(
                lambda item: (getattr(item, 'name_translated'), getattr(item, 'parent_name_internal')),
                self._name_translated, self._parent_name_internal
                )
        except QgistActionFound:
            return

    def disconnect(self):

        if not self._present:
            return

        self._action, self._present = None, False

    def _create_id(self):

        if len(self._name_translated) == 0:
            prefix = translate('global', '[unnamed]')
        else:
            prefix = '"%s"' % self._name_translated

        suffix = ', '.join([
            item for item in (self._name_internal, self._parent_name_internal) if len(item) > 0
            ])

        self._id = prefix
        if len(suffix) > 0:
             self._id += ' (%s)' % suffix

    @property
    def action(self):

        return self._action

    @action.setter
    def action(self, value):

        raise QgistAttributeError(translate('global', '"action" must not be changed. (dtype_action action)'))

    @property
    def id(self):

        return self._id

    @id.setter
    def id(self, value):

        raise QgistAttributeError(translate('global', '"id" must not be changed. (dtype_action id)'))

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

    @property
    def present(self):

        return self._present

    @present.setter
    def present(self, value):

        raise QgistAttributeError(translate('global', '"present" must not be changed. (dtype_action present)'))

    def as_dict(self):

        return dict(
            name_internal = self._name_internal,
            name_translated = self._name_translated,
            parent_name_internal = self._parent_name_internal,
            )

    @staticmethod
    def all_from_mainwindow(mainwindow):

        if not isinstance(mainwindow, QMainWindow):
            raise QgistTypeError(translate('global', '"mainwindow" must be a QGis mainwindow. (dtype_action all_from_mainwindow)'))

        return [
            dtype_action_class.from_action(action) for action in mainwindow.findChildren(QAction)
            ]

    @staticmethod
    def filter_unnamed(action_list):

        if not isinstance(action_list, list):
            raise QgistTypeError(translate('global', '"action_list" must be a list. (dtype_action filter_unnamed)'))
        if not all([isinstance(action, dtype_action_class) for action in action_list]):
            raise QgistTypeError(translate('global', 'Items in "action_list" must be of type dtype_action_class. (dtype_action filter_unnamed)'))

        named = []
        unnamed = []
        for action in action_list:
            if len(action.name_internal) == 0 and len(action.name_translated) == 0:
                unnamed.append(action)
            else:
                named.append(action)

        return named, unnamed

    @staticmethod
    def find_in_list(action_list, mainwindow):

        if not isinstance(action_list, list):
            raise QgistTypeError(translate('global', '"action_list" must be a list. (dtype_action find_in_list)'))
        if not all([isinstance(action, dtype_action_class) for action in action_list]):
            raise QgistTypeError(translate('global', 'Items in "action_list" must be of type dtype_action_class. (dtype_action find_in_list)'))
        if not isinstance(mainwindow, QMainWindow):
            raise QgistTypeError(translate('global', '"mainwindow" must be a QGis mainwindow. (dtype_action find_in_list)'))

        all_actions = dtype_action_class.all_from_mainwindow(mainwindow)

        for action in action_list:
            try:
                action.find(all_actions)
                self._toolbar.addAction(action.action)
            except (QgistActionConfusionError, QgistActionNotFoundError) as e:
                msg_warning(e, mainwindow)

    @staticmethod
    def from_action(action):

        if not isinstance(action, QAction):
            raise QgistTypeError(translate('global', '"action" must be a QAction. (dtype_action from_action)'))

        return dtype_action_class(
            name_internal = str(action.objectName()),
            name_translated = str(action.text()),
            parent_name_internal = str(action.parent().objectName()),
            action = action,
            )
