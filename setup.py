from cx_Freeze import setup, Executable

setup(name='sudoku.py',
      version='0.1',
      description='sudoku game',
      executables=[Executable("Solver.py", base="Win32GUI")]
      )
