from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import json
from chess_board import ChessBoard
import asyncio
from typing import Dict
import logging

app = FastAPI()

# 静态文件和模板配置
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 存储所有游戏会话
games: Dict[str, ChessBoard] = {}
# 存储WebSocket连接
connections: Dict[str, Dict[str, WebSocket]] = {}

# 配置日志
logging.basicConfig(
    filename='chess_game.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'  # 添加UTF-8编码设置
)

# 添加文件处理器和控制台处理器
file_handler = logging.FileHandler('chess_game.log', encoding='utf-8')  # 添加UTF-8编码
console_handler = logging.StreamHandler()

# 设置控制台处理器的编码
import sys
sys.stdout.reconfigure(encoding='utf-8')  # 修改控制台输出编码

# 创建格式化器
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 获取根记录器并添加处理器
logger = logging.getLogger()
logger.addHandler(file_handler)
logger.addHandler(console_handler)

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("chess.html", {"request": request})

@app.websocket("/ws/{game_id}/{player}")
async def websocket_endpoint(websocket: WebSocket, game_id: str, player: str):
    await websocket.accept()
    logger.info(f"Game {game_id} - Player {player} connected")

    # 初始化游戏
    if game_id not in games:
        games[game_id] = ChessBoard()
        connections[game_id] = {}
        logger.info(f"New game created: {game_id}")

    connections[game_id][player] = websocket

    try:
        while True:
            message = await websocket.receive_text()
            data = json.loads(message)

            # 处理日志消息
            if data["type"] == "log":
                logger.info(f"Game {game_id} - Player {player}: {data['message']}")
                continue

            # 处理移动消息
            if data["type"] == "move":
                game = games[game_id]
                from_pos = tuple(data["from"])
                to_pos = tuple(data["to"])

                logger.info(f"Game {game_id} - Player {player} - Move attempt: from {from_pos} to {to_pos}")

                if game.move_piece(from_pos, to_pos):
                    # 记录成功的移动
                    logger.info(f"Game {game_id} - Player {player} - Move successful: {from_pos} -> {to_pos}")

                    # 广播移动信息
                    move_data = {
                        "type": "move",
                        "from": from_pos,
                        "to": to_pos,
                        "current_player": game.current_player
                    }

                    for ws in connections[game_id].values():
                        await ws.send_json(move_data)

                    # 检查游戏是否结束
                    if game.is_king_captured(game.current_player):
                        winner = "white" if game.current_player == "black" else "black"
                        logger.info(f"Game {game_id} - Game over, winner: {winner}")
                        end_data = {
                            "type": "game_over",
                            "winner": winner
                        }
                        for ws in connections[game_id].values():
                            await ws.send_json(end_data)
                else:
                    logger.warning(f"Game {game_id} - Player {player} - Invalid move: {from_pos} -> {to_pos}")

    except WebSocketDisconnect:
        logger.info(f"Game {game_id} - Player {player} disconnected")
        connections[game_id].pop(player, None)
        if not connections[game_id]:
            logger.info(f"Game {game_id} - No players left, removing game")
            games.pop(game_id, None)
            connections.pop(game_id, None)
    except Exception as e:
        logger.error(f"Game {game_id} - Error: {str(e)}", exc_info=True)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
