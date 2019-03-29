import os
import sys
import random
import interfacing

class AutoChess(object):

    def __init__(self, ContestantA, ContestantB):

        self.CompleteChessBoard = dict()
        for contestant in [ContestantA, ContestantB]:
            if contestant.colour is 'white':
                BackRow, FrontRow = 0, 1
                contestant.enpassantrow = 4
            else:
                BackRow, FrontRow = 7, 6
                contestant.enpassantrow = 3

            contestant.longrook  = (BackRow, 0)
            contestant.longrook_target = \
            (contestant.longrook[0], contestant.longrook[1]+3)
            
            contestant.shortrook = (BackRow, 7)
            contestant.shortrook_target = \
            (contestant.shortrook[0], contestant.shortrook[1]-2)
            

            [self.CompleteChessBoard.setdefault((FrontRow,x), ChessPiece('p', (FrontRow,x), contestant)) \
            for x in range(8)]
            [self.CompleteChessBoard.setdefault((BackRow,x), ChessPiece('r', (BackRow,x), contestant)) \
            for x in [0,7]]
            [self.CompleteChessBoard.setdefault((BackRow,x), ChessPiece('kn',(BackRow,x), contestant)) \
            for x in [1,6]]
            [self.CompleteChessBoard.setdefault((BackRow,x), ChessPiece('b', (BackRow,x), contestant)) \
            for x in [2,5]]
            self.CompleteChessBoard.setdefault((BackRow,3),  ChessPiece('q', (BackRow,3), contestant))
            self.CompleteChessBoard.setdefault((BackRow,4),  ChessPiece('k', (BackRow,4), contestant))


    def ReloadChessBoard(self, contestant):
        if contestant.colour is 'white':
            ContestantA, ContestantB = contestant, contestant.opponent
        else:
            ContestantA, ContestantB = contestant.opponent, contestant
        os.system('clear')
        print "   Now playing: %s vs %s" % (ContestantA, ContestantB)
        self.PrintChessBoard()



        

    def PrintChessBoard(self):

        topbottom=['*','a','b','c','d','e','f','g','h','*']
        sides=['1','2','3','4','5','6','7','8']
        tbspacer=' '*6
        rowspacer=' '*5
        cellspacer=' '*4
        empty=' '*3

        print
        for field in topbottom:
            print "%4s" % field,
        print

        print tbspacer+("_"*4+' ')*8

        for row in range(8):
            print(rowspacer+(('|'+cellspacer)*9))
            print "%4s" % sides[row],('|'),
            for col in range(8):
                if (row, col) not in self.CompleteChessBoard:
                    print empty+'|',
                else:
                    print "%2s" % self.CompleteChessBoard[(row, col)],('|'),
            print "%2s" % sides[row],
            print
            print rowspacer+'|'+(("_"*4+'|')*8)
        print

        for field in topbottom:
            print "%4s" % field,

        print "\n"

    

    def ChessPlay(self, contestant):

        self.ReloadChessBoard(contestant)

        while True:

            print contestant.ContestantTurn(self.CompleteChessBoard)

            try:
                start, target = contestant.ReturnValidMove(self.CompleteChessBoard)
                print("start of if")
                if contestant.nature is 'AI':
                    interfacing.finalpositions(start,target)
                    interfacing.invalidmoveflag(0)
                    print("end of if in chess play")
                print("......")
                print(start)
                print(target)
            except (IndexError, ValueError):
                self.ReloadChessBoard(contestant)
                print "\n\nPlease enter a valid move."
                interfacing.invalidmoveflag(1)
                interfacing.invalidswap()
                print("////")
                print(interfacing.matrix1)
                print(interfacing.initial)
                

            except TypeError:
                # No start, target if user exit
                break

            else:
                if target in self.CompleteChessBoard or self.CompleteChessBoard[start].piecename is 'p':
                    Contestant.dullmoves = 0
                else:
                    Contestant.dullmoves += 1

                contestant.DoMovements(self.CompleteChessBoard, start, target)
                contestant.playedturns += 1

                # Check if there is a Pawn up for promotion
                if self.CompleteChessBoard[target].piecename is 'p':
                    if self.CompleteChessBoard[target].CanPawnPromoted():
                        contestant.DoPawnPromotion(self.CompleteChessBoard, target)

                contestant = contestant.opponent

                if contestant.CheckDraw(self.CompleteChessBoard):
                    return 1, contestant

                elif contestant.VerifyCheckMate(self.CompleteChessBoard):
                    return 2, contestant

                else:
                    self.ReloadChessBoard(contestant)

    def ChessEnd(self, contestant, result):

        looser = contestant.name
        winner = contestant.opponent.name

        if result == 1:
            endstring = "\n%s and %s reached a draw." % (winner, looser)
        elif result == 2:
            endstring = "\n%s put %s in checkmate." % (winner, looser)

        os.system('clear')
        self.PrintChessBoard()

        return endstring


    

class ChessPiece(object):

    def __init__(self, piecename, position, contestant):
        self.colour    = contestant.colour
        self.nature    = contestant.nature
        self.piecename = piecename
        self.position  = position
        self.nmbrofmoves = 0

    def __str__(self):
        if self.colour is 'white':
            if self.piecename is 'p':
                return 'WP'
            else:
                return self.piecename.upper()
        else:
            return self.piecename

    def CanPawnPromoted(self):
        if str(self.position[0]) in '07':
            return True

    def PromotePawn(self, to):
        self.piecename = to.lower()




class Contestant(object):

    allsquares = [(x, y) for x in range(8) for y in range(8)]
    dullmoves = 0

    def __init__(self, colour, nature, name):

        self.colour   = colour
        self.nature   = nature
        self.name     = name
        self.can_castle_long_this_turn  = False
        self.can_castle_short_this_turn = False
        self.playedturns = 0

    def __str__(self):
        if self.nature is 'AI':
            return self.name+' ('+self.nature+')'+' as '+self.colour
        else:
            return self.name+' as '+self.colour

    def SetContestantOpponent(self, opponent):
        self.opponent = opponent

    def FindPiecesPos(self, CompleteChessBoard):
        return [pos for pos in CompleteChessBoard if CompleteChessBoard[pos].colour is self.colour]

    def FindTargetPos(self, playerspieces):
        return [pos for pos in self.allsquares if pos not in playerspieces]

    def FindKingPosition(self, CompleteChessBoard):
        for mine in self.FindPiecesPos(CompleteChessBoard):
            if CompleteChessBoard[mine].piecename is 'k':
                return mine

    def validmoves(self, CompleteChessBoard):
        self.VerifyCastling(CompleteChessBoard)

        mypieces=self.FindPiecesPos(CompleteChessBoard)
        for mine in mypieces:
            for target in self.FindTargetPos(mypieces):
                if self.CanPieceMove(CompleteChessBoard, mine, target):
                    if not self.VerifyMoves(mine, target, CompleteChessBoard):
                        yield (mine, target)

    def VerifyCastling(self, CompleteChessBoard):
        FindKingPosition = self.FindKingPosition(CompleteChessBoard)
        if self.CanKingCastle(CompleteChessBoard, FindKingPosition):

            if self.CanLongRookCastle(CompleteChessBoard, FindKingPosition):
                self.can_castle_long_this_turn = True
            else:
                self.can_castle_long_this_turn = False

            if self.CanShortRookCastle(CompleteChessBoard, FindKingPosition):
                self.can_castle_short_this_turn = True
            else:
                self.can_castle_short_this_turn = False
        else:
            self.can_castle_long_this_turn = False
            self.can_castle_short_this_turn = False

    def CanKingCastle(self, CompleteChessBoard, FindKingPosition):
        if CompleteChessBoard[FindKingPosition].nmbrofmoves is 0 and not self.isincheck(CompleteChessBoard):
            return True

    def CanLongRookCastle(self, CompleteChessBoard, FindKingPosition):
        if self.longrook in CompleteChessBoard and CompleteChessBoard[self.longrook].nmbrofmoves is 0:
            if self.CheckClearPath(self.longrook, FindKingPosition, CompleteChessBoard):
                tmptarget = (FindKingPosition[0],FindKingPosition[1]-1)
                if not self.VerifyMoves(FindKingPosition, tmptarget, CompleteChessBoard):
                    return True

    def CanShortRookCastle(self, CompleteChessBoard, FindKingPosition):
        if self.shortrook in CompleteChessBoard and CompleteChessBoard[self.shortrook].nmbrofmoves is 0:
            if self.CheckClearPath(self.shortrook, FindKingPosition, CompleteChessBoard):
                tmptarget = (FindKingPosition[0],FindKingPosition[1]+1)
                if not self.VerifyMoves(FindKingPosition, tmptarget, CompleteChessBoard):
                    return True

    def GetInputPositions(self, initial,final):
        startcol  = initial[1]
        startrow  = initial[0]
        targetcol = final[1]
        targetrow = final[0]
        start     = (startrow, startcol)
        target    = (targetrow, targetcol)

        return start, target

    def CheckDraw(self, CompleteChessBoard):

        if not list(self.validmoves(CompleteChessBoard)) and not self.isincheck(CompleteChessBoard):
            return True

        if len(list(self.FindPiecesPos(CompleteChessBoard))) == \
           len(list(self.opponent.FindPiecesPos(CompleteChessBoard))) == 1:
            return True

        if Contestant.dullmoves/2 == 50:
            if self.nature is 'AI':
                return True
            else:
                if raw_input("Call a draw? (yes/no) : ") in ['yes','y','Yes']:
                    return True

    def VerifyCheckMate(self, CompleteChessBoard):

        if not list(self.validmoves(CompleteChessBoard)) and self.isincheck(CompleteChessBoard):
            return True

    def ContestantTurn(self, CompleteChessBoard):
       
        turnstring = "\n%s's Turn," % self.name
        warning = " *** Your King is in check *** "

        if self.isincheck(CompleteChessBoard):
            turnstring = turnstring + warning

        return turnstring

    def ReturnValidMove(self, CompleteChessBoard):

        print "\n"
        while True:

            # If contestant is computer, get a move from computer
            if self.nature is 'AI':
                #return aiengine.getAImove(self, CompleteChessBoard)
                #return random.choice(list(self.validmoves(CompleteChessBoard)))
                ailist=list(self.validmoves(CompleteChessBoard))
                print (ailist)
                f=0
                st,tr=[],[]
                rndmmove=[]
                while(f==0):
                    print("beginning of while")
                    #return random.choice(list(self.validmoves(CompleteChessBoard)))
                    
                    rndmmove=random.choice(ailist)
                    print rndmmove
                    print rndmmove[0],rndmmove[1]
                    print rndmmove[0][0],rndmmove[1][0]
                    
                    x1,y1,x2,y2=rndmmove[0][0],rndmmove[0][1],rndmmove[1][0],rndmmove[1][1]
                    if( ( x1==x2 and ( abs(y2-y1)!=0) ) or ( y1==y2 and ( abs(x2-x1)!=0) ) or ( abs(x2-x1) == abs(y2-y1) ) ):
                        st,tr=rndmmove[0],rndmmove[1]
                        f=1
                        
                #print ("st and tr are",st,tr)
                #x=raw_input()
                return st,tr
            
            else:
                # Contestant is human, get a move from input
                # move=raw_input("\nEnter your move : ")
                initial,final=interfacing.checkinterface()
                start, target = self.GetInputPositions(initial,final)
                print("HUMAN")
                print(start,target)
                if (start, target) in self.validmoves(CompleteChessBoard):
                    interfacing.swapmatrix()      
                    return start, target
                else:
                    raise IndexError

                #if move == 'exit':
                #    break

                #else:
                #   start, target = self.GetInputPositions(move)
                    #if (start, target) in self.validmoves(CompleteChessBoard):
                     #   return start, target
                    #else:
                     #   raise IndexError

    def VerifyMoves(self, start, target, CompleteChessBoard):
        # Make temporary move to test for check
        self.DoMovements(CompleteChessBoard, start, target)

        retval = self.isincheck(CompleteChessBoard)
        
        # Undo temporary move
        self.UndoMovements(CompleteChessBoard, start, target)

        return retval

    def isincheck(self, CompleteChessBoard):
        FindKingPosition = self.FindKingPosition(CompleteChessBoard)
        for enemy in self.opponent.FindPiecesPos(CompleteChessBoard):
            if self.opponent.CanPieceMove(CompleteChessBoard, enemy, FindKingPosition):
                return True

    def DoMovements(self, CompleteChessBoard, start, target):

        self.savedtargetpiece = None
        if target in CompleteChessBoard:
            self.savedtargetpiece = CompleteChessBoard[target]

        CompleteChessBoard[target] = CompleteChessBoard[start]
        CompleteChessBoard[target].position = target
        del CompleteChessBoard[start]

        CompleteChessBoard[target].nmbrofmoves += 1

        if CompleteChessBoard[target].piecename is 'p' and not self.savedtargetpiece:

            if abs(target[0]-start[0]) == 2:
                CompleteChessBoard[target].turn_moved_twosquares = self.playedturns

            elif abs(target[1]-start[1]) == abs(target[0]-start[0]) == 1:
                # Pawn has done en passant, remove the victim
                if self.colour is 'white':
                    passant_victim = (target[0]-1, target[1])
                else:
                    passant_victim = (target[0]+1, target[1])
                self.savedpawn = CompleteChessBoard[passant_victim]
                del CompleteChessBoard[passant_victim]

        if CompleteChessBoard[target].piecename is 'k':
            if target[1]-start[1] == -2:
                # King is castling long, move longrook
                self.DoMovements(CompleteChessBoard, self.longrook, self.longrook_target)
            elif target[1]-start[1] == 2:
                # King is castling short, move shortrook
                self.DoMovements(CompleteChessBoard, self.shortrook, self.shortrook_target)

    def UndoMovements(self, CompleteChessBoard, start, target):

        CompleteChessBoard[start] = CompleteChessBoard[target]
        CompleteChessBoard[start].position = start
        if self.savedtargetpiece:
            CompleteChessBoard[target] = self.savedtargetpiece
        else:
            del CompleteChessBoard[target]

        CompleteChessBoard[start].nmbrofmoves -= 1

        if CompleteChessBoard[start].piecename is 'p' and not self.savedtargetpiece:

            if abs(target[0]-start[0]) == 2:
                del CompleteChessBoard[start].turn_moved_twosquares

            elif abs(target[1]-start[1]) == abs(target[0]-start[0]) == 1:
                # We have moved back en passant Pawn, restore captured Pawn
                if self.colour is 'white':
                    formerpos_passant_victim = (target[0]-1, target[1])
                else:
                    formerpos_passant_victim = (target[0]+1, target[1])
                CompleteChessBoard[formerpos_passant_victim] = self.savedpawn

        if CompleteChessBoard[start].piecename is 'k':
            if target[1]-start[1] == -2:
                # King's castling long has been unmoved, move back longrook
                self.UndoMovements(CompleteChessBoard, self.longrook, self.longrook_target)
            elif target[1]-start[1] == 2:
                # King's castling short has been unmoved, move back shortrook
                self.UndoMovements(CompleteChessBoard, self.shortrook, self.shortrook_target)

    def DoPawnPromotion(self, CompleteChessBoard, target):
        if self.nature is 'AI':
            # See if Knight makes opponent checkmate
            CompleteChessBoard[target].PromotePawn('kn')
            if self.opponent.VerifyCheckMate(CompleteChessBoard):
                return
            else:
                promoteto = 'q'
                
        else:
            promoteto = 'empty'
            while promoteto.lower() not in ['kn','q']:
                promoteto = \
                raw_input("You may Promote your pawn:\n[Kn]ight [Q]ueen : ")

        CompleteChessBoard[target].PromotePawn(promoteto)

    def CheckClearPath(self, start, target, CompleteChessBoard):

        startcol, startrow = start[1], start[0]
        targetcol, targetrow = target[1], target[0]

        if abs(startrow - targetrow) <= 1 and abs(startcol - targetcol) <= 1:
            # The base case
            return True
        else:
            if targetrow > startrow and targetcol == startcol:
                # Straight down
                tmpstart = (startrow+1,startcol)
            elif targetrow < startrow and targetcol == startcol:
                # Straight up
                tmpstart = (startrow-1,startcol)
            elif targetrow == startrow and targetcol > startcol:
                # Straight right
                tmpstart = (startrow,startcol+1)
            elif targetrow == startrow and targetcol < startcol:
                # Straight left
                tmpstart = (startrow,startcol-1)
            elif targetrow > startrow and targetcol > startcol:
                # Diagonal down right
                tmpstart = (startrow+1,startcol+1)
            elif targetrow > startrow and targetcol < startcol:
                # Diagonal down left
                tmpstart = (startrow+1,startcol-1)
            elif targetrow < startrow and targetcol > startcol:
                # Diagonal up right
                tmpstart = (startrow-1,startcol+1)
            elif targetrow < startrow and targetcol < startcol:
                # Diagonal up left
                tmpstart = (startrow-1,startcol-1)

            # If no pieces in the way, test next square
            if tmpstart in CompleteChessBoard:
                return False
            else:
                return self.CheckClearPath(tmpstart, target, CompleteChessBoard)

    def CanPieceMove(self, CompleteChessBoard, start, target):

        startpiece = CompleteChessBoard[start].piecename.upper()

        if startpiece == 'R' and not self.RookConditionCheck(start, target):
            return False
        elif startpiece == 'KN' and not self.KnightConditionCheck(start, target):
            return False
        elif startpiece == 'P' and not self.PawnConditionCheck(start, target, CompleteChessBoard):
            return False
        elif startpiece == 'B' and not self.BishopConditionCheck(start, target):
            return False
        elif startpiece == 'Q' and not self.QueenConditionCheck(start, target):
            return False
        elif startpiece == 'K' and not self.KingConditionCheck(start, target):
            return False

        # Only the 'Knight' may jump over pieces
        if startpiece in 'RPBQK':
            if not self.CheckClearPath(start, target, CompleteChessBoard):
                return False

        return True

    def RookConditionCheck(self, start, target):

        # Check for straight lines of movement(start/target on same axis)
        if start[0] == target[0] or start[1] == target[1]:
            return True

    def KnightConditionCheck(self, start, target):

        # 'Knight' may move 2+1 in any direction and jump over pieces
        if abs(target[0]-start[0]) == 2 and abs(target[1]-start[1]) == 1:
            return True
        elif abs(target[0]-start[0]) == 1 and abs(target[1]-start[1]) == 2:
            return True

    def PawnConditionCheck(self, start, target, CompleteChessBoard):

        # Disable backwards and sideways movement
        if 'white' in self.colour and target[0] < start[0]:
            return False
        elif 'black' in self.colour and target[0] > start[0]:
            return False
        if start[0] == target[0]:
            return False

        if target in CompleteChessBoard:
            # Only attack if one square diagonaly away
            if abs(target[1]-start[1]) == abs(target[0]-start[0]) == 1:
                return True
        else:
            # Make peasants move only one forward (except first move)
            if start[1] == target[1]:
                # Normal one square move
                if abs(target[0]-start[0]) == 1:
                    return True
                # 1st exception to the rule, 2 square move first time
                if CompleteChessBoard[start].nmbrofmoves is 0:
                    if abs(target[0]-start[0]) == 2:
                        return True

            # 2nd exception to the rule, en passant
            if start[0] == self.enpassantrow:
                if abs(target[0]-start[0]) == 1:
                    if abs(target[1]-start[1]) == 1:
                        if target[1]-start[1] == -1:
                            passant_victim = (start[0], start[1]-1)
                        elif target[1]-start[1] == 1:
                            passant_victim = (start[0], start[1]+1)
                        if passant_victim in CompleteChessBoard and \
                        CompleteChessBoard[passant_victim].colour is not self.colour and \
                        CompleteChessBoard[passant_victim].piecename is 'p'and \
                        CompleteChessBoard[passant_victim].nmbrofmoves == 1 and \
                        CompleteChessBoard[passant_victim].turn_moved_twosquares == \
                        self.playedturns-1:
                            return True

    def BishopConditionCheck(self, start, target):

        # Check for non-horizontal/vertical and linear movement
        if abs(target[1]-start[1]) == abs(target[0]-start[0]):
            return True

    def QueenConditionCheck(self, start, target):

        # Will be true if move can be done as Rook or Bishop
        if self.RookConditionCheck(start, target) or self.BishopConditionCheck(start, target):
            return True

    def KingConditionCheck(self, start, target):

        # King can move one square in any direction
        if abs(target[0]-start[0]) <= 1 and abs(target[1]-start[1]) <= 1:
            return True

        # ..except when castling
        if self.can_castle_short_this_turn:
            if target[1]-start[1] == 2 and start[0] == target[0]:
                return True

        if self.can_castle_long_this_turn:
            if target[1]-start[1] == -2 and start[0] == target[0]:
                return True


def NewChessGame():

    os.system('clear')

    print """
      Welcome to AUTOMATED CHESS
      """

    ContestantA, ContestantB = GetContestants()
    ContestantA.SetContestantOpponent(ContestantB)
    ContestantB.SetContestantOpponent(ContestantA)

    game = AutoChess(ContestantA, ContestantB)

    infostring = \
    """
    %s and %s, let's play.
    
    Contestant A: %s
    Contestant B: %s 
     """
    print infostring % (ContestantA.name, ContestantB.name, ContestantA, ContestantB)

    #raw_input("\n\nPress Enter when ready")

    # WHITE starts
    contestant = ContestantA

    try:
        result, contestant = game.ChessPlay(contestant)

    except TypeError:
        # No result if user exit
        pass

    else:
        print game.ChessEnd(contestant, result)
        raw_input("\n\nPress any key to continue")

def GetContestants():

    ContestantA=Contestant('white','human','HUMAN')
    ContestantB=Contestant('black','AI','AI')
    return ContestantA, ContestantB

def main():
    
    menu="""
    Thanks for playing AUTOMATED CHESS, would you like to go again?
    Press Enter to play again or type 'exit'.  """
    
    try:
        while True:
            interfacing.initialize()
            NewChessGame()

            choice=raw_input(menu)

            if choice == 'exit':
                print "\n Welcome back!"
                break

    except KeyboardInterrupt:
        sys.exit("\n\n Aborting.")


if __name__ == '__main__':
    main()
