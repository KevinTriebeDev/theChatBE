import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .models import Chat


@require_http_methods(["GET", "POST"])
def chat_view(request):
	if request.method == "GET":
		chats = Chat.objects.order_by("created_at")
		data = [
			{
				"id": chat.id,
				"name": chat.name,
				"message": chat.message,
				"created_at": chat.created_at,
			}
			for chat in chats
		]
		return JsonResponse(data, safe=False)

	try:
		payload = json.loads(request.body)
	except json.JSONDecodeError:
		return JsonResponse({"error": "Ungültiges JSON."}, status=400)

	name = str(payload.get("name", "")).strip()
	message = str(payload.get("message", "")).strip()

	if not name or not message:
		return JsonResponse(
			{"error": "name und message sind erforderlich."},
			status=400,
		)

	chat = Chat.objects.create(name=name, message=message)
	return JsonResponse(
		{
			"id": chat.id,
			"name": chat.name,
			"message": chat.message,
			"created_at": chat.created_at,
		},
		status=201,
	)
