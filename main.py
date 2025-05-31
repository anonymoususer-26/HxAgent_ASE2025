from core.session import Session, NoIterativePlanningSession, NoShortTermNoExpSession, NoExpSession, LiEtAlSession
from error import InvalidConfiguration
from dataset import *
import argparse

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="HxAgent experimental program")
    parser.add_argument("-d", "--dataset", type=str, default="real_world_application", help="the dataset to run on; possible values include: 'real_world_application' (default) and 'miniwob'")
    parser.add_argument("-m", "--mode", type=int, default=1, help="1 for main session; 2 for no iterative planning; 3 for no short term and no experience; 4 for no experience")
    parser.add_argument("-p", "--playback", action='store_true', help="set to playback mode, use cautiously")
    parser.add_argument("-E", "--eval_only", action='store_true', help="set to omit the training phase, use cautiously")
    parser.add_argument("-t", "--train_instance", type=int, default=25, help="number of instances to train on a task")
    parser.add_argument("-e", "--eval_instance", type=int, default=25, help="number of instances to evaluate on a task")
    parser.add_argument("-i", "--task_id", type=str, default="all", help="id of the task to run experiment on (default to run all tasks in the specified dataset)")
    parser.add_argument("-r", "--randomize", action='store_true', help="setting this might cause unfair evaluation across ablation experiment as evaluation task would be randomized")
    
    args = parser.parse_args()

    task_factories = []
    if args.dataset == "real_world_application":
        if args.task_id == "all":
            task_factories = get_all_popular_task_factories()
        else:
            task_factories = [get_popular_task_factory_by_id(args.task_id)]
    elif args.dataset == "miniwob":
        if args.task_id == "all":
            task_factories = get_all_miniwob_task_factories()
        else:
            task_factories = [get_miniwob_task_factory_by_id(args.task_id)]
    else:
        raise InvalidConfiguration()

    for task_factory in task_factories:
        session = None
        if (args.randomize):
            task_factory.randomize = True

        if args.mode == 1:
            session = Session(task_factory)
        elif args.mode == 2:
            session = NoIterativePlanningSession(task_factory)
        elif args.mode == 3:
            session = NoShortTermNoExpSession(task_factory)
        elif args.mode == 4:
            session = NoExpSession(task_factory)
        elif args.mode == 5:
            session = LiEtAlSession(task_factory)
        else:
            raise InvalidConfiguration()

        if args.playback:
            session.playback()
        else:
            if not args.eval_only:
                session.train(args.train_instance)
            session.evaluate(args.eval_instance)
        