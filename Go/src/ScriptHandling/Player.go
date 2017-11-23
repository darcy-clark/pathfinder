package ScriptHandling

type Player struct {
    xPosition int
    yPosition int
    xPositionPrevious int
    yPositionPrevious int
    status PlayerStatus
}

type PlayerStatus int

const(
    ALIVE PlayerStatus = iota
    DEAD
    BLOCKED
)

var playerStatusName = [...]string {
    ALIVE: "alive",
    DEAD: "dead",
    BLOCKED: "blocked",
}

func (r PlayerStatus) String() string { return playerStatusName[r] }

func (r Player) GetXPosition() int {
    return r.xPosition
}

func (r Player) GetYPosition() int {
    return r.yPosition
}

func (r Player) GetXPositionPrevious() int {
    return r.xPositionPrevious
}

func (r Player) GetYPositionPrevious() int {
    return r.yPositionPrevious
}

func (r Player) GetStatus() PlayerStatus {
    return r.status
}

func (r *Player) SetStatus(status PlayerStatus) {
    r.status = status
}

func (r *Player) UpdatePosition(direction string) {
    r.xPositionPrevious = r.xPosition
    r.yPositionPrevious = r.yPosition

    switch direction {
    case "up":
        r.yPosition--
    case "down":
        r.yPosition++
    case "right":
        r.xPosition++
    case "left":
        r.xPosition--
    }
}

func (r *Player) RevertLastMove() {
    r.xPosition = r.xPositionPrevious
    r.yPosition = r.yPositionPrevious
}

