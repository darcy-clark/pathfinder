package ScriptHandling

import(
    "fmt"
)

type GameBoardGenerator struct {
    variable int
}

func (r *GameBoardGenerator) SetVariable(variable int) {
    r.variable = variable
}

func (r GameBoardGenerator) GetVariable() int {
    return r.variable
}

func (r GameBoardGenerator) Generate(xPosPlayer []int, yPosPlayer []int,
        xPosEnemy []int, yPosEnemy []int, xPosObstacle []int,
        yPosObstacle []int, previousBoard GameBoard) {

    gameBoard := previousBoard
    if previousBoard.GetBoard() == nil {
        board := make([][]string, previousBoard.GetSize())
        for i := range board {
            board[i] = make([]string, previousBoard.GetSize())
        }
        gameBoard.SetBoard(board)

        playerStatusMap := make(map[string][2]int)
        gameBoard.SetCharacterStatusMap(playerStatusMap)
    }

    gameBoard.Populate(xPosObstacle, yPosObstacle, "o")
    gameBoard.Populate(xPosEnemy, yPosEnemy, "e")
    gameBoard.Populate(xPosPlayer, yPosPlayer, "p")
    fmt.Println(gameBoard.GetBoard())
    fmt.Println(gameBoard)
}

