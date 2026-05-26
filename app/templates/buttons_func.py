
def toggle_pause(paused):
    paused = not paused
    if paused:
        button_pause.label.set_text("Resume")
        animation.event_source.stop()
    else:
        button_pause.label.set_text("Pause")
        animation.event_source.start()

def toggle_infection_mode(manual_infection_mode):
    manual_infection_mode = not manual_infection_mode
    if manual_infection_mode:
        button_infect.label.set_text("Click Map")
    else:
        button_infect.label.set_text("Add Infection")


