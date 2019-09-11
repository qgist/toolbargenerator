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
    QListWidgetItem,
    QToolBar,
    )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .const import SEPARATOR
from .error import (
    QgistActionConfusionError,
    QgistActionNotFoundError,
    )
from ..error import (
    QgistAttributeError,
    QgistTypeError,
    QgistValueError,
    )
from ..msg import msg_warning
from ..util import translate


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS: ACTION
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
        if name_internal == '' and name_translated == SEPARATOR and parent_name_internal == '':
            raise QgistValueError(translate('global', 'Names suggest that this is a separator, not an action. (dtype_action)'))

        self._name_internal = name_internal
        self._name_translated = name_translated
        self._parent_name_internal = parent_name_internal
        self._action = action

        self._create_id()

    def __eq__(self, other_action):

        if not isinstance(other_action, dtype_action_class):
            raise QgistTypeError(translate('global', '"other_action" must be of type dtype_action. (dtype_action eq)'))

        if all([
            len(self.name_translated) > 0,
            len(other_action.name_translated) > 0,
            len(self.name_internal) > 0,
            len(other_action.name_internal) > 0,
            len(self.parent_name_internal) > 0,
            len(other_action.parent_name_internal) > 0,
            ]):
            if all([
                self.name_translated == other_action.name_translated,
                self.name_internal == other_action.name_internal,
                self.parent_name_internal == other_action.parent_name_internal,
                ]):
                return 10

        if all([
            len(self.name_translated) > 0,
            len(other_action.name_translated) > 0,
            len(self.name_internal) > 0,
            len(other_action.name_internal) > 0,
            ]):
            if all([
                self.name_translated == other_action.name_translated,
                self.name_internal == other_action.name_internal,
                ]):
                return 9

        if all([
            len(self.name_internal) > 0,
            len(other_action.name_internal) > 0,
            len(self.parent_name_internal) > 0,
            len(other_action.parent_name_internal) > 0,
            ]):
            if all([
                self.name_internal == other_action.name_internal,
                self.parent_name_internal == other_action.parent_name_internal,
                ]):
                return 8

        if all([
            len(self.name_translated) > 0,
            len(other_action.name_translated) > 0,
            len(self.parent_name_internal) > 0,
            len(other_action.parent_name_internal) > 0,
            ]):
            if all([
                self.name_translated == other_action.name_translated,
                self.parent_name_internal == other_action.parent_name_internal,
                ]):
                return 7

        if len(self.name_internal) > 0 and len(other_action.name_internal) > 0:
            if self.name_internal == other_action.name_internal:
                return 6

        if len(self.name_translated) > 0 and len(other_action.name_translated) > 0:
            if self.name_translated == other_action.name_translated:
                return 5

        return 0

    def add_to_toolbar(self, toolbar):

        if not isinstance(toolbar, QToolBar):
            raise QgistTypeError(translate('global', '"toolbar" must be a QToolBar. (dtype_action add_to_toolbar)'))

        if self._action is not None:
            toolbar.addAction(self._action)

    def find(self, all_actions):

        if not isinstance(all_actions, list):
            raise QgistTypeError(translate('global', '"all_actions" must be a list. (dtype_action find)'))
        if not all([isinstance(item, dtype_action_class) for item in all_actions]):
            raise QgistTypeError(translate('global', 'Items in "all_actions" must be of type dtype_action. (dtype_action find)'))

        self._action = None

        rank_list = [
            (rank, action) for rank, action in
            ((self == action, action) for action in all_actions)
            if rank > 0
            ]

        if len(rank_list) == 0:
            raise QgistActionNotFoundError(translate('global', 'Action could not be found. (dtype_action find)'))

        rank_dict = {rank: list() for rank in range(5, 11)}
        for rank, action in rank_list:
            rank_dict[rank].append(action)

        for rank in range(10, 4, -1):

            if len(rank_dict[rank]) == 0:
                continue

            if len(rank_dict[rank]) > 1:
                try:
                    raise QgistActionConfusionError(
                        '{RANK:d}|{TRANSLATED:s}|{INTERNAL:s}|{PARENT:s}: '.format(
                            RANK = rank,
                            TRANSLATED = self._name_translated,
                            INTERNAL = self._name_internal,
                            PARENT = self._parent_name_internal,
                            ) + translate('global', 'Confused, multiple matching actions. (dtype_action find)')
                        )
                except QgistActionConfusionError as e:
                    msg_warning(e)

            self._action = rank_dict[rank][0].action
            return

        raise QgistActionConfusionError(translate('global', 'Confused, something odd happened. (dtype_action find)'))

    def disconnect(self):

        if self._action is None:
            return

        self._action = None

    def _create_id(self):

        if len(self._name_translated) == 0:
            prefix = translate('global', '[unnamed]')
        else:
            prefix = '%s' % self._name_translated

        suffix = ', '.join([
            item for item in (self._name_internal, self._parent_name_internal) if len(item) > 0
            ])

        self._id = prefix
        if len(suffix) > 0:
             self._id += ' (%s)' % suffix

        self._id = self._id.replace('&', '')

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

        return self._action is not None

    @present.setter
    def present(self, value):

        raise QgistAttributeError(translate('global', '"present" must not be changed. (dtype_action present)'))

    def as_dict(self):

        return dict(
            name_internal = self._name_internal,
            name_translated = self._name_translated,
            parent_name_internal = self._parent_name_internal,
            )

    def as_listwidgetitem(self):

        item = QListWidgetItem(self._id)
        if self._action is not None:
            item.setIcon(self._action.icon())

        return item

    @staticmethod
    def all_from_mainwindow(mainwindow):

        if not isinstance(mainwindow, QMainWindow):
            raise QgistTypeError(translate('global', '"mainwindow" must be a QGis mainwindow. (dtype_action all_from_mainwindow)'))

        return [
            dtype_action_class.from_action(action) for action in mainwindow.findChildren(QAction)
            ]

    @staticmethod
    def all_named_from_mainwindow_as_dict(mainwindow, with_separator = True):

        if not isinstance(mainwindow, QMainWindow):
            raise QgistTypeError(translate('global', '"mainwindow" must be a QGis mainwindow. (dtype_action all_named_from_mainwindow_as_dict)'))
        if not isinstance(with_separator, bool):
            raise QgistTypeError(translate('global', '"with_separator" must be a bool. (dtype_action all_named_from_mainwindow_as_dict)'))

        named_actions, _ = dtype_action_class.filter_unnamed(
            dtype_action_class.all_from_mainwindow(mainwindow)
            )

        mainwindow_actions = {action.id: action for action in named_actions}

        if with_separator:
            sep = dtype_separator_class()
            mainwindow_actions[sep.id] = sep

        return mainwindow_actions

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

    @staticmethod
    def from_dict(action_dict):

        if not isinstance(action_dict, dict):
            raise QgistTypeError(translate('global', '"action_dict" must be a dict. (dtype_action from_dict)'))

        if all([
            action_dict['name_internal'] == '',
            action_dict['name_translated'] == SEPARATOR,
            action_dict['parent_name_internal'] == '',
            ]):
            return dtype_separator_class(**action_dict)
        else:
            return dtype_action_class(**action_dict)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS: SEPARATOR
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class dtype_separator_class(dtype_action_class):

    def __init__(self, *args, **kwargs):

        self._name_internal = ''
        self._name_translated = SEPARATOR
        self._id = SEPARATOR
        self._parent_name_internal = ''
        self._action = None

    def add_to_toolbar(self, toolbar):

        if not isinstance(toolbar, QToolBar):
            raise QgistTypeError(translate('global', '"toolbar" must be a QToolBar. (dtype_separator add_to_toolbar)'))

        toolbar.addSeparator()

    def find(self, all_actions):
        pass

    def disconnect(self):
        pass
