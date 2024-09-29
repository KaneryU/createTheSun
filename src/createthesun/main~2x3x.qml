import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt.labs.platform
import "./qml/" as Kyu




ApplicationWindow {
    id: root
    visible: true
    minimumWidth: 840
    minimumHeight: 480

    title: "Create The Sun"
    property QtObject tabsModel // absract list model from python -- contains tabs
    
    Connections {
        target: Backend

        function onLoadComplete() {
            console.log("Loaded")
            console.log(ItemsModel)
            console.log(Backend.activeTab)
        }
    }

    Connections {
        target: Theme
    }


    
    background: Rectangle {
        id: background
        color: Theme.background

        Behavior on color {
            ColorAnimation {
                easing.type: Easing.InOutQuad
                duration: 200
            }
        }
    }
    
    header: Text {
        id: headertext
        
        text: root.title
        font.pixelSize: 24

        color: Theme.primary
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter

        Behavior on color {
            ColorAnimation {
                easing.type: Easing.InOutQuad
                duration: 200
            }
        }
    }

    Item {
        id: content
        anchors.fill: parent
        anchors.top: header.bottom
        anchors.topMargin: 10
        anchors.bottomMargin: 10
        anchors.leftMargin: 10
        anchors.rightMargin: 10

        ListView {
            id: tabBar
            model: root.tabsModel
            
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top

            height: (43 / 2) + 10

            orientation: ListView.Horizontal
            
            spacing: 2
            delegate: Rectangle {
                id: rect
                topRightRadius: 10/2
                topLeftRadius: 10/2

                width: metrics.width + 10
                height: 43 / 2

                color: (Backend.activeTab == model.internalName) ? Theme.primaryContainer : Theme.surfaceContainer

                border.color: (Backend.activeTab == model.internalName) ? Theme.primaryFixedDim : Theme.primaryFixed
                border.width: 1/2

                Text {
                    id: tabText
                    text: model.name
                    color: (Backend.activeTab == model.internalName) ? Theme.onPrimaryContainer : Theme.onSurface
                    font.pixelSize: 18
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    anchors.fill: parent

                    Behavior on color {
                        ColorAnimation {
                            easing.type: Easing.InOutQuad
                            duration: 200
                        }
                    }
                }

                TextMetrics {
                    id: metrics
                    text: tabText.text
                    font: tabText.font
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: Backend.activeTab = model.internalName
                }

                Behavior on color {
                    ColorAnimation {
                        easing.type: Easing.InOutQuad
                        duration: 200
                    }
                }
            }
        }
        StackLayout {
            id: tabContent
            anchors.top: tabBar.bottom
            anchors.left: parent.left
            anchors.right: electrons.left
            anchors.bottom: parent.bottom

            currentIndex: Backend.tabList.indexOf(Backend.activeTab)

            Item {
                Loader {
                    id: tabLoader
                    anchors.fill: parent
                    source: "qml/tabs/" + Backend.activeTab + ".qml"
                    asynchronous: true
                    visible: status == Loader.Ready
                }
            }
        }

        Item {
            id: electrons

            anchors.top: tabBar.bottom
            anchors.right: parent.right

            anchors.bottom: parent.bottom

            width: 52/2
            
            anchors.leftMargin: 10

            Loader {
                id: electronLoader
                anchors.fill: parent
                source: "qml/electrons.qml"

            }
        }
    }
}