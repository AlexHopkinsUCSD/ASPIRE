from app.domain.models.student import StudentKnowledgeCreate

from ..database.repositories.trigger_event import TriggerEventRepository
from app.domain.protocols.repositories.trigger_event import TriggerEventRepository as TriggerEventRepoProtocol
from ..database.repositories.student import StudentKnowledgeRepository
import time
import logging 
import asyncio
from threading import Thread

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def start_process_worker():
    process_manger = Process_Manager(max_batch_size=100)
    worker = Thread(target=process_manger.worker)
    worker.start()

class Process_Manager:
    def __init__(self, max_batch_size: int = 250):
        self.max_batch_size = max_batch_size
        self.event_repo: TriggerEventRepoProtocol = TriggerEventRepository()
        self.s_k_repo = StudentKnowledgeRepository()

    def worker(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(self.start())
        loop.close()

    async def start(self):
        paused = True
        while True:
            queue_exists = await self.event_repo.queue_check()

            if queue_exists:
                if paused:
                    logger.info("Processing trigger events")
                    paused = False

                events = await self.event_repo.get_queue(max_batch_size=self.max_batch_size)
                await self.run(events=events)

            else:
                if not paused:
                    paused = True
                    logger.info("Queue empty process paused")

                time.sleep(60)

    async def run(self, events):
            if not events:
                logger.info("No events to process")
            else:
                for event in events:
                    try:
                        score = await self.s_k_repo.get(student_id=event.student_id, concept_name=event.concept)
                        new_score = (event.numerator + score.score) / (event.denominator + 1)
                        await self.s_k_repo.update(StudentKnowledgeCreate(student_id=event.student_id, concept_name=event.concept, score=new_score))
                        await self.event_repo.bulk_delete(event_ids=event.event_ids)

                    except Exception as e:
                        new_score = event.numerator / event.denominator
                        await self.s_k_repo.add(StudentKnowledgeCreate(student_id=event.student_id, concept_name=event.concept, score=new_score))
                        await self.event_repo.bulk_delete(event_ids=event.event_ids)

