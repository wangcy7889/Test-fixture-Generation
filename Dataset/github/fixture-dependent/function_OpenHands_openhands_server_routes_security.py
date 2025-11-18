from fastapi import APIRouter, HTTPException, Request, Response, status
app = APIRouter(prefix='/api/conversations/{conversation_id}')

@app.route('/security/{path:path}', methods=['GET', 'POST', 'PUT', 'DELETE'])
async def security_api(request: Request) -> Response:
    if not request.state.conversation.security_analyzer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Security analyzer not initialized')
    return await request.state.conversation.security_analyzer.handle_api_request(request)