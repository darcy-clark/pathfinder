package ScriptHandling

type GameBoardGenerator struct { }

func (r GameBoardGenerator) Generate(xPosPlayer []int, yPosPlayer []int,
        xPosEnemy []int, yPosEnemy []int, xPosObstacle []int,
        yPosObstacle []int, previousBoard GameBoard) GameBoard {

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
    return gameBoard
}

