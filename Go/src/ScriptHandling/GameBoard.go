package ScriptHandling

import(
    "fmt"
)

type GameBoard struct {
    characterStatusMap map[string][2]int
    board [][]string
    size int
}

func (r GameBoard) GetCharachterStatusMap() map[string][2]int {
    return r.characterStatusMap
}

func (r *GameBoard) SetCharacterStatusMap(characterStatusMap map[string][2]int) {
    r.characterStatusMap = characterStatusMap
}

func (r GameBoard) GetBoard() [][]string {
    return r.board
}

func (r *GameBoard) SetBoard(board [][]string) {
    r.board = board
}

func (r GameBoard) GetSize() int {
    return r.size
}

func (r *GameBoard) SetSize(size int) {
    r.size = size
}

func (r *GameBoard) Populate(xPos []int, yPos []int, nextBoardPiece string) {
    for i := range xPos {
        x := xPos[i]
        y := yPos[i]

        currentBoardPiece := &r.board[x][y]
        // If a player moves onto an enemy, the player gets sent to death [-1, -1]
        if *currentBoardPiece == "e" && nextBoardPiece == "p" {
            r.characterStatusMap[fmt.Sprintf("%s%d", "p", i)] = [2]int{-1, -1}
            continue
        // If a player moves onto an obstacle, do nothing. Do not move player
        } else if *currentBoardPiece == "o" && nextBoardPiece == "p" {
            continue
        } else if nextBoardPiece != "o" {
            r.characterStatusMap[fmt.Sprintf("%s%d", nextBoardPiece, i)] = [2]int{x, y}
        }
        *currentBoardPiece = nextBoardPiece
    }
}

