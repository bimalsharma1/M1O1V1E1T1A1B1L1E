import LookForTable
import GoToTable
import GoToOppositeSideOfTable
import MoveTable
import LiftTable
import LandTable
import PositionToCentreOfTableSide
import SmallStepSideways

class MoveTableMain:
    """description of class"""
    def Main(self, motionProxy, portName1, X, Y, Theta):

        lookForTable = LookForTable.LookForTable() 
        lookForTable.LookForTable(motionProxy, portName1)

        goToTable = GoToTable.GoToTable()
        goToTable.GoToTable(motionProxy, portName1)

        moveTable = MoveTable.MoveTable()
        moveTable.MoveTable(motionProxy, X, Y, Theta)
        #    moveTableWithTwoRobots.Main(motionProxy, 0, 2, 0)
        #LookForTable.LookForTable(motionProxy)
        #GoToTable.GoToTable(motionProxy)
        #MoveTable.MoveTable(motionProxy, X, Y, Theta)



