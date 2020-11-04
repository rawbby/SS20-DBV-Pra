#  Copyright (c) 2020 Robert Andreas Fritsch
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import sys

from PySide2.QtWidgets import QApplication, QMainWindow

from dbvpra.gui.Control_window import Control_window
from dbvpra.gui.Ui_window import Ui_window

if __name__ == '__main__':
    # app entry point

    app = QApplication(sys.argv)
    window = QMainWindow()

    ui = Ui_window()
    ui.setupUi(window)
    ui.retranslateUi(window)

    control = Control_window()
    control.setupControl(ui, window)

    window.show()
    sys.exit(app.exec_())
