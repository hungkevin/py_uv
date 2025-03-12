from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import json
from chess_board import ChessBoard
import asyncio
from typing import Dict

app = FastAPI()

# 静态文件和模板配置
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 存储所有游戏会话
games: Dict[str, ChessBoard] = {}
# 存储WebSocket连接
connections: Dict[str, Dict[str, WebSocket]] = {}

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("chess.html", {"request": request})

@app.websocket("/ws/{game_id}/{player}")
async def websocket_endpoint(websocket: WebSocket, game_id: str, player: str):
    await websocket.accept()

    # 初始化游戏
    if game_id not in games:
        games[game_id] = ChessBoard()
        connections[game_id] = {}

    connections[game_id][player] = websocket

    try:
        while True:
            data = await websocket.receive_json()
            game = games[game_id]

            if data["type"] == "move":
                from_pos = tuple(data["from"])
                to_pos = tuple(data["to"])

                if game.move_piece(from_pos, to_pos):
                    # 广播移动信息给所有玩家
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
                        end_data = {
                            "type": "game_over",
                            "winner": winner
                        }
                        for ws in connections[game_id].values():
                            await ws.send_json(end_data)

    except WebSocketDisconnect:
        connections[game_id].pop(player, None)
        if not connections[game_id]:
            games.pop(game_id, None)
            connections.pop(game_id, None)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
