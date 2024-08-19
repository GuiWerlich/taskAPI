from rest_framework.views import APIView, Response, status
from .models import Task
from .serializers import TaskSerializer
from datetime import datetime
from .permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class TaskView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def post(self, request):
        serializer = TaskSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        task = serializer.save()
        serializer = TaskSerializer(task)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    def get(self, request, task_id=None):
        
        if task_id is not None:

            try:
                task = Task.objects.get(id=task_id, is_deleted=False)

            except Task.DoesNotExist:
                return Response({"message": "Task Not Found"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = TaskSerializer(task)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            tasks = Task.objects.filter(is_deleted=False)

            due_date = request.query_params.get('due_date')
            title = request.query_params.get('title')

            if due_date:
                try:
                    due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
                except ValueError:
                    return Response({"message": "Invalid due_date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST) 
        
                if not tasks.filter(due_date=due_date).exists() :
                    return Response({"message": "No tasks found with the given due_date"}, status=status.HTTP_404_NOT_FOUND)
                tasks = tasks.filter(due_date=due_date)

            if title:
                tasks = tasks.filter(title__icontains=title)
                if not tasks.exists():
                    return Response({"message": "No tasks found with the given title"}, status=status.HTTP_404_NOT_FOUND)
                

        serializer = TaskSerializer(tasks, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, task_id):

        try:
            task = Task.objects.get(id=task_id, is_deleted=False)

        except Task.DoesNotExist:
            return Response({"message": "Task Not Found"}, status=status.HTTP_404_NOT_FOUND)
        
        if not request.data:
            return Response({"message": "No data provided. Accepted fields: title, description, due_date"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = TaskSerializer(task, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
           
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def delete(self, request, task_id):

        try:
            task = Task.objects.get(id=task_id, is_deleted=False)

        except Task.DoesNotExist:
            return Response({"message": "Task Not Found"}, status=status.HTTP_404_NOT_FOUND)       
        
        task.is_deleted = True
        task.save()

        return Response({"message": "Task deleted successfully."}, status=status.HTTP_204_NO_CONTENT)




        

