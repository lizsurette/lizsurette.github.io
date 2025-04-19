class SudokuGame {
    constructor() {
        this.board = Array(9).fill().map(() => Array(9).fill(0));
        this.solution = Array(9).fill().map(() => Array(9).fill(0));
        this.fixed = Array(9).fill().map(() => Array(9).fill(false));
        this.candidates = Array(9).fill().map(() => Array(9).fill().map(() => new Set()));
        this.showCandidates = false;
        this.selectedCell = null;
        this.init();
    }

    init() {
        this.createBoard();
        this.setupEventListeners();
        this.generateNewGame();
    }

    createBoard() {
        const board = document.getElementById('sudoku-board');
        board.innerHTML = '';
        
        for (let i = 0; i < 81; i++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.dataset.index = i;
            board.appendChild(cell);
        }
    }

    setupEventListeners() {
        const board = document.getElementById('sudoku-board');
        board.addEventListener('click', (e) => {
            if (e.target.classList.contains('cell')) {
                this.selectCell(e.target);
            }
        });

        document.getElementById('new-game').addEventListener('click', () => {
            this.generateNewGame();
        });

        document.getElementById('check-solution').addEventListener('click', () => {
            this.checkSolution();
        });

        document.getElementById('toggle-candidates').addEventListener('click', () => {
            this.toggleCandidates();
        });

        // Add number pad
        const numberPad = document.createElement('div');
        numberPad.className = 'number-pad';
        for (let i = 1; i <= 9; i++) {
            const button = document.createElement('button');
            button.textContent = i;
            button.addEventListener('click', () => {
                if (this.selectedCell) {
                    this.setNumber(i);
                }
            });
            numberPad.appendChild(button);
        }
        board.parentNode.insertBefore(numberPad, board.nextSibling);

        // Add keyboard support
        document.addEventListener('keydown', (e) => {
            if (this.selectedCell) {
                const num = parseInt(e.key);
                if (num >= 1 && num <= 9) {
                    this.setNumber(num);
                } else if (e.key === 'Backspace' || e.key === 'Delete') {
                    this.setNumber(0);
                }
            }
        });
    }

    selectCell(cell) {
        if (this.selectedCell) {
            this.selectedCell.classList.remove('selected');
        }
        this.selectedCell = cell;
        cell.classList.add('selected');
        this.highlightRelatedCells(cell);
    }

    highlightRelatedCells(cell) {
        // Remove previous highlights
        document.querySelectorAll('.cell.highlighted').forEach(c => {
            c.classList.remove('highlighted');
        });

        const index = parseInt(cell.dataset.index);
        const row = Math.floor(index / 9);
        const col = index % 9;

        // Highlight row
        for (let i = 0; i < 9; i++) {
            const rowCell = document.querySelector(`[data-index="${row * 9 + i}"]`);
            if (rowCell !== cell) {
                rowCell.classList.add('highlighted');
            }
        }

        // Highlight column
        for (let i = 0; i < 9; i++) {
            const colCell = document.querySelector(`[data-index="${i * 9 + col}"]`);
            if (colCell !== cell) {
                colCell.classList.add('highlighted');
            }
        }

        // Highlight 3x3 box
        const boxRow = Math.floor(row / 3) * 3;
        const boxCol = Math.floor(col / 3) * 3;
        for (let i = 0; i < 3; i++) {
            for (let j = 0; j < 3; j++) {
                const boxCell = document.querySelector(`[data-index="${(boxRow + i) * 9 + (boxCol + j)}"]`);
                if (boxCell !== cell) {
                    boxCell.classList.add('highlighted');
                }
            }
        }
    }

    setNumber(num) {
        if (!this.selectedCell) return;
        
        const index = parseInt(this.selectedCell.dataset.index);
        const row = Math.floor(index / 9);
        const col = index % 9;

        if (this.fixed[row][col]) return;

        this.board[row][col] = num;
        this.selectedCell.textContent = num || '';
        this.selectedCell.classList.remove('invalid');
        
        // Clear candidates for this cell
        this.candidates[row][col].clear();
        this.updateCandidatesDisplay();
        
        if (num !== 0) {
            this.validateMove(row, col);
        }

        // Update candidates for related cells
        this.updateCandidates();
    }

    validateMove(row, col) {
        const num = this.board[row][col];
        let isValid = true;

        // Check row
        for (let i = 0; i < 9; i++) {
            if (i !== col && this.board[row][i] === num) {
                isValid = false;
                document.querySelector(`[data-index="${row * 9 + i}"]`).classList.add('invalid');
            }
        }

        // Check column
        for (let i = 0; i < 9; i++) {
            if (i !== row && this.board[i][col] === num) {
                isValid = false;
                document.querySelector(`[data-index="${i * 9 + col}"]`).classList.add('invalid');
            }
        }

        // Check 3x3 box
        const boxRow = Math.floor(row / 3) * 3;
        const boxCol = Math.floor(col / 3) * 3;
        for (let i = 0; i < 3; i++) {
            for (let j = 0; j < 3; j++) {
                const r = boxRow + i;
                const c = boxCol + j;
                if (r !== row && c !== col && this.board[r][c] === num) {
                    isValid = false;
                    document.querySelector(`[data-index="${r * 9 + c}"]`).classList.add('invalid');
                }
            }
        }

        if (!isValid) {
            this.selectedCell.classList.add('invalid');
        }
    }

    updateCandidates() {
        for (let row = 0; row < 9; row++) {
            for (let col = 0; col < 9; col++) {
                if (this.board[row][col] === 0) {
                    this.candidates[row][col].clear();
                    for (let num = 1; num <= 9; num++) {
                        if (this.isValidCandidate(row, col, num)) {
                            this.candidates[row][col].add(num);
                        }
                    }
                } else {
                    this.candidates[row][col].clear();
                }
            }
        }
        this.updateCandidatesDisplay();
    }

    isValidCandidate(row, col, num) {
        // Check row
        for (let i = 0; i < 9; i++) {
            if (i !== col && this.board[row][i] === num) {
                return false;
            }
        }

        // Check column
        for (let i = 0; i < 9; i++) {
            if (i !== row && this.board[i][col] === num) {
                return false;
            }
        }

        // Check 3x3 box
        const boxRow = Math.floor(row / 3) * 3;
        const boxCol = Math.floor(col / 3) * 3;
        for (let i = 0; i < 3; i++) {
            for (let j = 0; j < 3; j++) {
                const r = boxRow + i;
                const c = boxCol + j;
                if (r !== row && c !== col && this.board[r][c] === num) {
                    return false;
                }
            }
        }

        return true;
    }

    updateCandidatesDisplay() {
        for (let row = 0; row < 9; row++) {
            for (let col = 0; col < 9; col++) {
                const cell = document.querySelector(`[data-index="${row * 9 + col}"]`);
                let candidatesDiv = cell.querySelector('.candidates');
                
                if (!candidatesDiv) {
                    candidatesDiv = document.createElement('div');
                    candidatesDiv.className = 'candidates';
                    cell.appendChild(candidatesDiv);
                }

                candidatesDiv.innerHTML = '';
                if (this.board[row][col] === 0) {
                    for (let i = 1; i <= 9; i++) {
                        const span = document.createElement('span');
                        span.textContent = this.candidates[row][col].has(i) ? i : '';
                        candidatesDiv.appendChild(span);
                    }
                }

                candidatesDiv.classList.toggle('hidden', !this.showCandidates || this.board[row][col] !== 0);
            }
        }
    }

    toggleCandidates() {
        this.showCandidates = !this.showCandidates;
        this.updateCandidatesDisplay();
    }

    generateNewGame() {
        // Clear the board
        this.board = Array(9).fill().map(() => Array(9).fill(0));
        this.fixed = Array(9).fill().map(() => Array(9).fill(false));
        this.candidates = Array(9).fill().map(() => Array(9).fill().map(() => new Set()));
        
        // Generate a solved board
        this.generateSolution();
        
        // Remove numbers based on difficulty
        const difficulty = document.getElementById('difficulty').value;
        const cellsToRemove = {
            'easy': 30,
            'medium': 40,
            'hard': 50
        }[difficulty];

        // Copy solution to board
        this.board = this.solution.map(row => [...row]);
        
        // Remove numbers
        let removed = 0;
        while (removed < cellsToRemove) {
            const row = Math.floor(Math.random() * 9);
            const col = Math.floor(Math.random() * 9);
            if (this.board[row][col] !== 0) {
                this.board[row][col] = 0;
                removed++;
            }
        }

        // Mark fixed numbers
        for (let i = 0; i < 9; i++) {
            for (let j = 0; j < 9; j++) {
                this.fixed[i][j] = this.board[i][j] !== 0;
            }
        }

        this.updateDisplay();
        this.updateCandidates();
    }

    generateSolution() {
        const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9];
        
        const shuffle = (array) => {
            for (let i = array.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [array[i], array[j]] = [array[j], array[i]];
            }
            return array;
        };

        const isValid = (row, col, num) => {
            // Check row
            for (let i = 0; i < 9; i++) {
                if (this.solution[row][i] === num) return false;
            }

            // Check column
            for (let i = 0; i < 9; i++) {
                if (this.solution[i][col] === num) return false;
            }

            // Check 3x3 box
            const boxRow = Math.floor(row / 3) * 3;
            const boxCol = Math.floor(col / 3) * 3;
            for (let i = 0; i < 3; i++) {
                for (let j = 0; j < 3; j++) {
                    if (this.solution[boxRow + i][boxCol + j] === num) return false;
                }
            }

            return true;
        };

        const solve = (row, col) => {
            if (col === 9) {
                row++;
                col = 0;
            }
            if (row === 9) return true;

            if (this.solution[row][col] !== 0) {
                return solve(row, col + 1);
            }

            const shuffledNumbers = shuffle([...numbers]);
            for (const num of shuffledNumbers) {
                if (isValid(row, col, num)) {
                    this.solution[row][col] = num;
                    if (solve(row, col + 1)) return true;
                    this.solution[row][col] = 0;
                }
            }

            return false;
        };

        solve(0, 0);
    }

    updateDisplay() {
        const cells = document.querySelectorAll('.cell');
        cells.forEach(cell => {
            cell.classList.remove('fixed', 'invalid', 'selected', 'highlighted');
            cell.textContent = '';
        });

        for (let i = 0; i < 9; i++) {
            for (let j = 0; j < 9; j++) {
                const index = i * 9 + j;
                const cell = cells[index];
                const num = this.board[i][j];
                
                if (num !== 0) {
                    cell.textContent = num;
                    if (this.fixed[i][j]) {
                        cell.classList.add('fixed');
                    }
                }
            }
        }
    }

    checkSolution() {
        const message = document.getElementById('message');
        let isComplete = true;
        let isCorrect = true;

        for (let i = 0; i < 9; i++) {
            for (let j = 0; j < 9; j++) {
                if (this.board[i][j] === 0) {
                    isComplete = false;
                }
                if (this.board[i][j] !== this.solution[i][j]) {
                    isCorrect = false;
                }
            }
        }

        if (!isComplete) {
            message.textContent = 'Please fill in all cells!';
            message.className = 'alert alert-warning';
        } else if (isCorrect) {
            message.textContent = 'Congratulations! You solved the puzzle!';
            message.className = 'alert alert-success';
        } else {
            message.textContent = 'Some numbers are incorrect. Keep trying!';
            message.className = 'alert alert-danger';
        }
        message.style.display = 'block';
    }
}

// Initialize the game when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new SudokuGame();
}); 