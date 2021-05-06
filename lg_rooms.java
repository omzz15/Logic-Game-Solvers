public class lg_rooms{
    int gridSize = 5;
    int[][] board = {
        {1,1,1,1,1},
        {1,1,1,1,1},
        {1,1,1,1,1},
        {1,1,1,1,1},
        {1,1,1,1,1}
    };
    Board b;

    lg_rooms(){
        b = new Board(gridSize, board);
    }

    public static void main(String[] args){
    }
}

class Node{
    Node[] neighbors = new Node[4];
    int sol;
    int row, col;
    Node(int row, int col, int sol){
        this.sol = sol;
        this.row = row;
        this.col = col;
    }

    int getCount(Dir d){
        if(neighbors[d.val] != null)return neighbors[d.val].getCount(d) + 1;
        return 0;
    }

    int getCurNum(){
        return getCount(Dir.UP) + getCount(Dir.DOWN) + getCount(Dir.LEFT) + getCount(Dir.RIGHT);
    }

    boolean isSolved(){
        if(sol == 0) return true;
        return getCurNum() == sol;
    }

    boolean isValid(Dir d){
        if(d != null) return getCurNum() - getCount(d) >= sol;
        else return getCurNum() >= sol;
    }

    int getNeighborCount(){
        int cnt = 0;
        for(Node n : neighbors) if(n != null) cnt++;
        return cnt;
    }

    int getNodeRank(){
        return sol + getNeighborCount();
    }

}

class Board{
    int gridSize;
    int[][] board;
    Node[][] ng;
    boolean solved = false;

    Board(int gridSize, int[][] board){
        this.gridSize = gridSize;
        this.board = board;
        ng = new Node[gridSize][gridSize];

        buildBoard();
    }

    void buildBoard(){
        for(int r = 0; r < gridSize; r++){
            for(int c = 0; c < gridSize; c++){
                ng[r][c] = new Node(r, c, board[r][c]);
                if(r > 0){
                    ng[r][c].neighbors[Dir.UP.val] = ng[r - 1][c];
                    ng[r - 1][c].neighbors[Dir.DOWN.val] = ng[r][c];
                }
                if(c > 0){
                    ng[r][c].neighbors[Dir.LEFT.val] = ng[r][c - 1];
                    ng[r][c - 1].neighbors[Dir.RIGHT.val] = ng[r][c];
                }
            }
        }
    }

    Node getLeastRank(){
        Node min = ng[0][0];
        for(int r = 0; r < gridSize; r++){
            for(int c = 0; c < gridSize; c++){
                if(ng[r][c].isSolved()) continue;
                if(ng[r][c].getNodeRank() < min.getNodeRank()) min = ng[r][c];
            }
        }
        return min;
    }

    boolean isSolved(){
        for(Node[] r : ng){
            for(Node n : r) if(!n.isSolved()) return false;
        }
        return true;
    }
}

enum Dir{
    UP(0),
    DOWN(2),
    LEFT(1),
    RIGHT(3);

    int val;

    Dir(int val){
        this.val = val;
    }
}