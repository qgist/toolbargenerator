# QGIST TOOLBARGENERATOR
# QGIS Plugin for Generating Toolbars
# https://github.com/qgist/toolbargenerator
#
#     makefile: Project makefile
#
#     Copyright (C) 2017-2019 QGIST project <info@qgist.org>
#
# <LICENSE_BLOCK>
# The contents of this file are subject to the GNU General Public License
# Version 2 ("GPL" or "License"). You may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt
# https://github.com/qgist/toolbargenerator/blob/master/LICENSE
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for the
# specific language governing rights and limitations under the License.
# </LICENSE_BLOCK>

release:
	make clean
	zip -r toolbargenerator.zip *
	gpg --detach-sign -a toolbargenerator.zip

clean:
	-rm toolbargenerator.zip*
	find qgist/ -name '*.pyc' -exec rm -f {} +
	find qgist/ -name '*.pyo' -exec rm -f {} +
	find qgist/ -name '*~' -exec rm -f {} +
	find ./ -name '__pycache__' -exec rm -fr {} +

translate:
	python3 -c "import makefile; makefile.translate()"
