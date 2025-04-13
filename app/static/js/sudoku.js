class SudokuGame {
    constructor() {
        this.grid = Array(9).fill().map(() => Array(9).fill(0));
        this.solution = Array(9).fill().map(() => Array(9).fill(0));
        this.difficulty = 'medium';
        this.showCandidates = false;
        this.candidates = Array(9).fill().map(() => Array(9).fill().map(() => new Set()));
        this.selectedNumber = null;
        this.setupEventListeners();
        this.init();
    }

    init() {
        this.generatePuzzle();
        this.renderGrid();
    }

    setupEventListeners() {
        document.getElementById('new-game').addEventListener('click', () => this.startNewGame());
        document.getElementById('check-solution').addEventListener('click', () => this.checkSolution());
        document.getElementById('show-solution').addEventListener('click', () => this.showSolution());
        document.getElementById('toggle-candidates').addEventListener('click', () => this.toggleCandidates());
        document.getElementById('difficulty').addEventListener('change', (e) => {
            this.difficulty = e.target.value;
            this.startNewGame();
        });
        
        // Add number selector event listeners
        document.querySelectorAll('.number-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const number = parseInt(e.target.dataset.number);
                
                // Remove selected class from all buttons
                document.querySelectorAll('.number-btn').forEach(b => b.classList.remove('selected'));
                
                // Handle clear button (0) separately
                if (number === 0) {
                    this.selectedNumber = 0; // Set to 0 instead of null to indicate eraser is selected
                    e.target.classList.add('selected');
                    console.log("Eraser selected");
                } else {
                    this.selectedNumber = number;
                    e.target.classList.add('selected');
                }
            });
        });
        
        // Log available number buttons for debugging
        console.log("Number buttons found:", document.querySelectorAll('.number-btn').length);
        document.querySelectorAll('.number-btn').forEach(btn => {
            console.log("Button:", btn.textContent, "data-number:", btn.dataset.number);
        });
    }

    generatePuzzle() {
        // Initialize grid with zeros
        this.grid = Array(9).fill().map(() => Array(9).fill(0));
        this.solution = Array(9).fill().map(() => Array(9).fill(0));
        this.candidates = Array(9).fill().map(() => Array(9).fill().map(() => new Set()));

        // Generate solution
        this.generateSolution(0, 0);

        // Copy solution to grid
        this.grid = this.solution.map(row => [...row]);

        // Remove numbers based on difficulty
        const cellsToRemove = {
            'easy': 30,
            'medium': 40,
            'hard': 50
        }[this.difficulty];

        this.removeNumbers(cellsToRemove);
    }

    generateSolution(row, col) {
        if (col === 9) {
            row++;
            col = 0;
        }
        if (row === 9) return true;

        if (this.solution[row][col] !== 0) {
            return this.generateSolution(row, col + 1);
        }

        const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9];
        this.shuffle(numbers);

        for (let num of numbers) {
            if (this.isValid(row, col, num)) {
                this.solution[row][col] = num;
                if (this.generateSolution(row, col + 1)) {
                    return true;
                }
                this.solution[row][col] = 0;
            }
        }

        return false;
    }

    isValid(row, col, num) {
        // Check row
        for (let x = 0; x < 9; x++) {
            if (this.solution[row][x] === num) return false;
        }

        // Check column
        for (let x = 0; x < 9; x++) {
            if (this.solution[x][col] === num) return false;
        }

        // Check 3x3 box
        let startRow = row - row % 3;
        let startCol = col - col % 3;
        for (let i = 0; i < 3; i++) {
            for (let j = 0; j < 3; j++) {
                if (this.solution[i + startRow][j + startCol] === num) return false;
            }
        }

        return true;
    }

    shuffle(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
    }

    removeNumbers(count) {
        let cells = [];
        for (let i = 0; i < 9; i++) {
            for (let j = 0; j < 9; j++) {
                cells.push([i, j]);
            }
        }
        this.shuffle(cells);

        for (let i = 0; i < count; i++) {
            const [row, col] = cells[i];
            this.grid[row][col] = 0;
        }
    }

    renderGrid() {
        const grid = document.getElementById('sudoku-grid');
        grid.innerHTML = '';

        for (let i = 0; i < 9; i++) {
            for (let j = 0; j < 9; j++) {
                const cellContainer = document.createElement('div');
                cellContainer.className = 'cell-container';
                
                // Add border classes for 3x3 boxes
                if (j % 3 === 0) cellContainer.classList.add('border-left');
                if (j % 3 === 2) cellContainer.classList.add('border-right');
                if (i % 3 === 0) cellContainer.classList.add('border-top');
                if (i % 3 === 2) cellContainer.classList.add('border-bottom');

                const input = document.createElement('input');
                input.type = 'number';
                input.className = 'cell-input';
                input.min = 1;
                input.max = 9;
                input.dataset.row = i;
                input.dataset.col = j;

                // Only set readOnly for initial puzzle numbers
                if (this.grid[i][j] !== 0 && this.isInitialNumber(i, j)) {
                    input.value = this.grid[i][j];
                    input.readOnly = true;
                    input.classList.add('initial');
                } else if (this.grid[i][j] !== 0) {
                    // For user-entered numbers, just set the value but don't make readOnly
                    input.value = this.grid[i][j];
                }

                const candidates = document.createElement('div');
                candidates.className = 'candidates';
                candidates.style.display = (this.showCandidates && this.grid[i][j] === 0) ? 'grid' : 'none';

                // Only create candidate elements for valid candidates
                if (this.grid[i][j] === 0) {
                    // Calculate valid candidates for this cell
                    const validCandidates = new Set();
                    for (let num = 1; num <= 9; num++) {
                        // Check if number exists in row
                        let inRow = false;
                        for (let col = 0; col < 9; col++) {
                            if (col !== j && this.grid[i][col] === num) {
                                inRow = true;
                                break;
                            }
                        }
                        
                        // Check if number exists in column
                        let inCol = false;
                        for (let row = 0; row < 9; row++) {
                            if (row !== i && this.grid[row][j] === num) {
                                inCol = true;
                                break;
                            }
                        }
                        
                        // Check if number exists in 3x3 box
                        let inBox = false;
                        const boxRow = Math.floor(i / 3) * 3;
                        const boxCol = Math.floor(j / 3) * 3;
                        for (let r = 0; r < 3; r++) {
                            for (let c = 0; c < 3; c++) {
                                if ((boxRow + r !== i || boxCol + c !== j) && 
                                    this.grid[boxRow + r][boxCol + c] === num) {
                                    inBox = true;
                                    break;
                                }
                            }
                            if (inBox) break;
                        }
                        
                        // Only add as candidate if it doesn't exist in row, column, or box
                        if (!inRow && !inCol && !inBox) {
                            validCandidates.add(num);
                        }
                    }
                    
                    // Create candidate elements only for valid candidates
                    for (let num of validCandidates) {
                        const candidate = document.createElement('div');
                        candidate.className = 'candidate active';
                        candidate.textContent = num;
                        candidates.appendChild(candidate);
                    }
                }

                cellContainer.appendChild(input);
                cellContainer.appendChild(candidates);
                grid.appendChild(cellContainer);

                input.addEventListener('input', (e) => this.handleInput(e));
                input.addEventListener('focus', (e) => this.handleFocus(e));
                input.addEventListener('blur', (e) => this.handleBlur(e));
            }
        }
    }

    handleInput(event) {
        const input = event.target;
        const value = input.value;
        const row = parseInt(input.dataset.row);
        const col = parseInt(input.dataset.col);
        
        if (value === '') {
            this.grid[row][col] = 0;
            input.classList.remove('incorrect');
        } else {
            const num = parseInt(value);
            if (num >= 1 && num <= 9) {
                this.grid[row][col] = num;
                input.classList.remove('incorrect');
            } else {
                input.value = '';
                this.grid[row][col] = 0;
            }
        }
        
        // Update candidates after cell value changes
        this.updateCandidates();
        
        // Check if puzzle is complete
        if (this.isPuzzleComplete()) {
            this.checkSolution();
        }
    }

    handleFocus(event) {
        const input = event.target;
        if (!input.readOnly) {
            input.classList.add('focused');
            
            // If a number is selected, automatically fill the cell
            if (this.selectedNumber !== null) {
                const row = parseInt(input.dataset.row);
                const col = parseInt(input.dataset.col);
                
                // If the selected number is 0 (eraser), remove the number from the cell
                if (this.selectedNumber === 0) {
                    this.grid[row][col] = 0;
                    input.value = '';
                    input.classList.remove('incorrect');
                } else {
                    this.grid[row][col] = this.selectedNumber;
                    input.value = this.selectedNumber;
                    input.classList.remove('incorrect');
                }
                
                this.updateCandidates();
            }
        }
    }

    handleBlur(event) {
        const input = event.target;
        input.classList.remove('focused');
    }

    startNewGame() {
        this.generatePuzzle();
        this.renderGrid();
        this.selectedNumber = null;
        document.querySelectorAll('.number-btn').forEach(btn => btn.classList.remove('selected'));
    }

    checkSolution() {
        let isCorrect = true;
        const inputs = document.querySelectorAll('#sudoku-grid input');

        inputs.forEach(input => {
            const row = parseInt(input.dataset.row);
            const col = parseInt(input.dataset.col);
            const value = parseInt(input.value) || 0;

            if (value !== this.solution[row][col]) {
                input.classList.add('incorrect');
                isCorrect = false;
            } else {
                input.classList.remove('incorrect');
            }
        });

        if (isCorrect) {
            alert('Congratulations! You solved the puzzle correctly!');
        }
    }

    showSolution() {
        const inputs = document.querySelectorAll('#sudoku-grid input');
        inputs.forEach(input => {
            const row = parseInt(input.dataset.row);
            const col = parseInt(input.dataset.col);
            input.value = this.solution[row][col];
            input.classList.remove('incorrect');
        });
    }

    toggleCandidates() {
        this.showCandidates = !this.showCandidates;
        const candidatesElements = document.querySelectorAll('.candidates');
        candidatesElements.forEach((el, index) => {
            const row = Math.floor(index / 9);
            const col = index % 9;
            el.style.display = (this.showCandidates && this.grid[row][col] === 0) ? 'grid' : 'none';
        });
        this.updateCandidates();
    }

    updateCandidates() {
        // Clear all candidates
        this.candidates = Array(9).fill().map(() => Array(9).fill().map(() => new Set()));

        // For each empty cell, find possible candidates
        for (let i = 0; i < 9; i++) {
            for (let j = 0; j < 9; j++) {
                if (this.grid[i][j] === 0) {
                    // Check each number 1-9
                    for (let num = 1; num <= 9; num++) {
                        // Check if number exists in row
                        let inRow = false;
                        for (let col = 0; col < 9; col++) {
                            if (col !== j && this.grid[i][col] === num) {
                                inRow = true;
                                break;
                            }
                        }
                        
                        // Check if number exists in column
                        let inCol = false;
                        for (let row = 0; row < 9; row++) {
                            if (row !== i && this.grid[row][j] === num) {
                                inCol = true;
                                break;
                            }
                        }
                        
                        // Check if number exists in 3x3 box
                        let inBox = false;
                        const boxRow = Math.floor(i / 3) * 3;
                        const boxCol = Math.floor(j / 3) * 3;
                        for (let r = 0; r < 3; r++) {
                            for (let c = 0; c < 3; c++) {
                                if ((boxRow + r !== i || boxCol + c !== j) && 
                                    this.grid[boxRow + r][boxCol + c] === num) {
                                    inBox = true;
                                    break;
                                }
                            }
                            if (inBox) break;
                        }
                        
                        // Only add as candidate if it doesn't exist in row, column, or box
                        if (!inRow && !inCol && !inBox) {
                            this.candidates[i][j].add(num);
                        }
                    }
                }
            }
        }

        // Re-render the grid to update candidate display
        this.renderGrid();
    }

    isPuzzleComplete() {
        // Check if all cells are filled
        for (let i = 0; i < 9; i++) {
            for (let j = 0; j < 9; j++) {
                if (this.grid[i][j] === 0) {
                    return false;
                }
            }
        }
        return true;
    }

    // Add a method to check if a number is part of the initial puzzle
    isInitialNumber(row, col) {
        // Check if this cell was part of the initial puzzle
        // We can determine this by checking if the number in the grid matches the solution
        // and if the cell was not empty in the initial grid
        return this.grid[row][col] === this.solution[row][col] && this.grid[row][col] !== 0;
    }
}

// Initialize the game when the page loads
document.addEventListener('DOMContentLoaded', () => {
    const game = new SudokuGame();
}); 