from maat import *
import datetime

def explore(m: MaatEngine):
    global save_next
    global state_manager

    # We keep exploring new paths as long as execution it stopped by reaching
    # SUCCESS_ADDR or FAILURE_ADDR
    while m.run() == STOP.HOOK:

        # Load the next state to explore into the engine.
        # dequeue_state() returns False is there are no more states to load
        if not state_manager.dequeue_state(m):
            break

        # When reloading a state, we set save_next to False. We do this
        # to avoid serialising the same state again when resuming execution.
        # The state we just loaded was about to branch, which means that one of both
        # possibilities (taken and not taken) has been explored already, and that the
        # other will get explored now. So there is no need to save that state again.
        save_next = False


def solve(m: MaatEngine):
    global save_next
    global state_manager
    print("PATH")

    # If we can successfully invert the condition of the current
    # branch, we save the current state for later exploration, and
    # take the other path first
    if save_next:
        # Check if we can invert the branch condition
        s = Solver()
        for c in m.path.constraints():
            s.add(c)
        if m.info.branch.taken:
            s.add(m.info.branch.cond.invert())
        else:
            s.add(m.info.branch.cond)
        if s.check():
            # We found a model that inverts the branch condition
            model = s.get_model()
            # Save current state for later execution
            state_manager.enqueue_state(m)
            # Update symbolic variables to explore the other path first
            m.vars.update_from(model)

    # We can skip only one branch when we just loaded a state, but then
    # we want to take save the next ones
    save_next = True

def explore_single_file(filepath,flag,level,exploration):
    start = datetime.datetime.now()
    m = MaatEngine(ARCH.X64, OS.LINUX)
    m.load(filepath,BIN.ELF64)
    stdin = m.env.fs.get_fa_by_handle(0)
    buf = m.vars.new_concolic_buffer(
    "input",
    b'aaaaaaaa',
    nb_elems=8,
    elem_size=1,
    trailing_value=ord('\n') # concrete new line at the end of the input
    )
    # Exploration hooks
    m.hooks.add(EVENT.PATH, WHEN.BEFORE, name="path", callbacks=[solve])
    #m.hooks.add(EVENT.EXEC, WHEN.BEFORE, name="fail", filter=FAILURE_ADDR)
    #m.hooks.add(EVENT.EXEC, WHEN.BEFORE, name="success", filter=SUCCESS_ADDR)
    # Explore
    #explore(m)
    end=datetime.datetime.now()
    print("time:{}",end-start)



explore_single_file("00_angr_find","","",True)
