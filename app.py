import streamlit as st
import streamlit.components.v1 as components
import time


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="4×4 N-Queens",
    page_icon="♛",
    layout="centered"
)


# ============================================================
# CONFIGURATION
# ============================================================

N = 4


# ============================================================
# SESSION STATE
# ============================================================

if "board" not in st.session_state:
    st.session_state.board = [[0] * N for _ in range(N)]

if "highlight" not in st.session_state:
    st.session_state.highlight = None

if "highlight_color" not in st.session_state:
    st.session_state.highlight_color = None

if "status" not in st.session_state:
    st.session_state.status = "Press Start"

if "speed" not in st.session_state:
    st.session_state.speed = 0.5


# ============================================================
# TITLE
# ============================================================

st.title("♛ 4×4 N-Queens Backtracking")

st.caption(
    "Watch the backtracking algorithm solve the N-Queens problem "
    "step by step."
)


# ============================================================
# DRAW BOARD
# ============================================================

def draw_board():

    board = st.session_state.board
    highlight = st.session_state.highlight
    highlight_color = st.session_state.highlight_color

    html = """
    <!DOCTYPE html>

    <html>

    <head>

        <meta charset="UTF-8">

        <style>

            * {
                box-sizing: border-box;
            }

            html, body {
                margin: 0;
                padding: 0;
                background: transparent;
            }

            .container {
                width: 100%;
                display: flex;
                justify-content: center;
            }

            .board {
                width: 400px;
                height: 400px;

                display: grid;

                grid-template-columns:
                    repeat(4, 100px);

                grid-template-rows:
                    repeat(4, 100px);

                border: 2px solid black;
            }

            .square {

                width: 100px;
                height: 100px;

                display: flex;

                align-items: center;
                justify-content: center;

                font-family: Arial, sans-serif;

                font-size: 58px;

                border: 1px solid black;

                user-select: none;
            }

            .light {
                background-color: #f0d9b5;
            }

            .dark {
                background-color: #b58863;
            }

        </style>

    </head>

    <body>

        <div class="container">

            <div class="board">
    """

    # --------------------------------------------------------
    # Squares
    # --------------------------------------------------------

    for r in range(N):

        for c in range(N):

            # Highlight square
            if highlight == (r, c):

                background = highlight_color

            # Normal chessboard colors
            elif (r + c) % 2 == 0:

                background = "#f0d9b5"

            else:

                background = "#b58863"

            # Queen
            if board[r][c]:

                queen = "♛"

            else:

                queen = ""

            html += f"""
                <div
                    class="square"
                    style="background-color: {background};"
                >
                    {queen}
                </div>
            """

    html += """
            </div>

        </div>

    </body>

    </html>
    """

    components.html(
        html,
        height=410,
        width=420,
        scrolling=False
    )


# ============================================================
# CHECK IF POSITION IS SAFE
# ============================================================

def safe(board, row, col):

    for r in range(row):

        # ----------------------------------------------------
        # Same column
        # ----------------------------------------------------

        if board[r][col]:
            return False

        # ----------------------------------------------------
        # Left diagonal
        # ----------------------------------------------------

        left_col = col - (row - r)

        if left_col >= 0:

            if board[r][left_col]:
                return False

        # ----------------------------------------------------
        # Right diagonal
        # ----------------------------------------------------

        right_col = col + (row - r)

        if right_col < N:

            if board[r][right_col]:
                return False

    return True


# ============================================================
# SOLVE
# ============================================================

def solve():

    board = st.session_state.board

    row = 0
    col = 0

    while True:

        # ====================================================
        # SOLUTION FOUND
        # ====================================================

        if row == N:

            st.session_state.status = "🎉 Solution Found!"

            st.session_state.highlight = None
            st.session_state.highlight_color = None

            draw_area.empty()

            with draw_area:
                draw_board()

            break


        # ====================================================
        # NO MORE COLUMNS
        # BACKTRACK
        # ====================================================

        if col == N:

            # We reached the first row and nothing worked
            if row == 0:

                st.session_state.status = "No solution"

                draw_area.empty()

                with draw_area:
                    draw_board()

                break


            # Go back one row
            row -= 1


            # Find the queen in that row
            for c in range(N):

                if board[row][c]:

                    # Remove queen
                    board[row][c] = 0

                    # Continue from next column
                    col = c + 1


                    # ----------------------------------------
                    # UI
                    # ----------------------------------------

                    st.session_state.status = (
                        f"Backtracking: Row {row + 1}"
                    )

                    st.session_state.highlight = (row, c)

                    st.session_state.highlight_color = "#cdb4db"


                    draw_area.empty()

                    with draw_area:
                        draw_board()


                    time.sleep(
                        st.session_state.speed
                    )

                    break

            continue


        # ====================================================
        # CHECK CURRENT POSITION
        # ====================================================

        if safe(board, row, col):

            # ------------------------------------------------
            # PLACE QUEEN
            # ------------------------------------------------

            board[row][col] = 1


            st.session_state.status = (
                f"Place queen: Row {row + 1}, "
                f"Column {col + 1}"
            )

            st.session_state.highlight = (row, col)

            st.session_state.highlight_color = "#b7e4c7"


            draw_area.empty()

            with draw_area:
                draw_board()


            time.sleep(
                st.session_state.speed
            )


            # Move to next row
            row += 1

            # Start from first column
            col = 0


        else:

            # ------------------------------------------------
            # CONFLICT
            # ------------------------------------------------

            st.session_state.status = (
                f"Conflict: Row {row + 1}, "
                f"Column {col + 1}"
            )

            st.session_state.highlight = (row, col)

            st.session_state.highlight_color = "#f4a6a6"


            draw_area.empty()

            with draw_area:
                draw_board()


            time.sleep(
                st.session_state.speed
            )


            # Try next column
            col += 1


# ============================================================
# CONTROLS
# ============================================================

speed = st.slider(
    "Speed",

    min_value=0.1,
    max_value=1.0,

    value=st.session_state.speed,

    step=0.1,

    help="Lower values make the algorithm faster."
)

st.session_state.speed = speed


# ============================================================
# STATUS
# ============================================================

st.write(
    f"**Status:** {st.session_state.status}"
)


# ============================================================
# BOARD
# ============================================================

draw_area = st.empty()

with draw_area:
    draw_board()


# ============================================================
# START BUTTON
# ============================================================

if st.button(
    "▶ Start",
    use_container_width=True,
    type="primary"
):

    # Reset board
    st.session_state.board = [
        [0] * N for _ in range(N)
    ]

    # Reset highlighting
    st.session_state.highlight = None
    st.session_state.highlight_color = None

    # Reset status
    st.session_state.status = "Starting..."


    # Draw empty board
    draw_area.empty()

    with draw_area:
        draw_board()


    # Start algorithm
    solve()