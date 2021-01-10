import streamlit as st
import numpy as np
from scipy import interpolate

class MovingObject():

    def __init__(
        self,
        coordinate_x = 0,
        coordinate_y = 0,
        coordinate_Vx = 0,
        coordinate_Vy = 0,
        halfmaxsize_x = 1,
        halfmaxsize_y = 1,
    ):
        self.coordinate_x = coordinate_x
        self.coordinate_y = coordinate_y
        self.coordinate_Vx = coordinate_Vx
        self.coordinate_Vy = coordinate_Vy
        self.halfmaxsize_x = halfmaxsize_x
        self.halfmaxsize_y = halfmaxsize_y
        self.body = self.get_body() 

    def get_body(self):
        body = np.random.choice([0, 1], size=(self.halfmaxsize_x*2, self.halfmaxsize_y*2))
        return body
    
    def change_coordinates(self, x0=0, y0=0, Vx=0, Vy=0, dt=1):
        x = np.int(x0 + Vx * dt)
        y = np.int(y0 + Vy * dt)
        return x, y
    
    def change_velocities(self, Vx0=0, Vy0=0, ax=0, ay=0, dt=1):
        Vx = Vx0 + ax * dt
        Vy = Vy0 + ay * dt
        return Vx, Vy

    def set_coordinates(self, x=None, y=None, Vx=None, Vy=None):
        if x is not None:
            self.coordinate_x = x
        if y is not None:
            self.coordinate_y = y
        if Vx is not None:
            self.coordinate_Vx = Vx
        if Vy is not None:
            self.coordinate_Vy = Vy
        


def run(n=960, m=640):
    field = np.zeros((m, n))

    x = np.random.randint(n)
    y = np.random.randint(m)
    Vx = 0.1
    Vy = 0.1
    
    object = MovingObject(
        coordinate_x=x,
        coordinate_y=y,
        coordinate_Vx=Vx,
        coordinate_Vy=Vy,
        halfmaxsize_x=10,
        halfmaxsize_y=10,
    )

    image = st.empty()
    progress_bar = st.sidebar.progress(0)
    frame_text = st.sidebar.empty()

    trace = np.zeros((m, n))
    trace_width = 2
    trace_hight = 2
    trace[
        object.coordinate_x - trace_width:object.coordinate_x + trace_width:, 
        object.coordinate_y - trace_hight:object.coordinate_y + trace_hight:, 
    ] = 1

    num_frames = 1000
    for frame_num in range(num_frames): 
        progress_bar.progress(frame_num/num_frames)
        frame_text.text("Frame %i/1000" % (frame_num + 1))

        Vx, Vy = object.change_velocities(
            Vx0=object.coordinate_Vx, 
            Vy0=object.coordinate_Vy, 
            #ax=np.random.randint(low=-1, high=1),
            #ay=np.random.randint(low=-1, high=1)
            ax=np.random.normal(0, 0.3),
            ay=np.random.normal(0, 0.3)
        )
        object.set_coordinates(Vx=Vx, Vy=Vy)

        x, y = object.change_coordinates(
            x0=object.coordinate_x,
            y0=object.coordinate_y,
            Vx=object.coordinate_Vx,
            Vy=object.coordinate_Vy,
        )
        object.set_coordinates(x=x, y=y)
        if object.coordinate_x - object.halfmaxsize_x < 0:
           object.set_coordinates(
               x=object.coordinate_x + np.absolute(object.coordinate_x - object.halfmaxsize_x),
               Vx=(-1) * object.coordinate_Vx,
            )

        if object.coordinate_x + object.halfmaxsize_x > m:
            object.set_coordinates(
                x=object.coordinate_x - np.absolute(m - object.coordinate_x - object.halfmaxsize_x),
                Vx=(-1) * object.coordinate_Vx 
            )

        if object.coordinate_y - object.halfmaxsize_y < 0:
            object.set_coordinates(
                y=object.coordinate_y + np.absolute(object.coordinate_y - object.halfmaxsize_y),
                Vy=(-1) * object.coordinate_Vy 
            )

        if object.coordinate_y + object.halfmaxsize_y > n:
            object.set_coordinates(
                y=object.coordinate_y - np.absolute(n - object.coordinate_y - object.halfmaxsize_y),
                Vy=(-1) * object.coordinate_Vy 
            )
        trace[
            object.coordinate_x - trace_width:object.coordinate_x + trace_width:, 
            object.coordinate_y - trace_hight:object.coordinate_y + trace_hight:, 
        ] = 1

        field = np.pad(
            object.body,
            (
                (object.coordinate_x - object.halfmaxsize_x, m - object.coordinate_x - object.halfmaxsize_x), 
                (object.coordinate_y - object.halfmaxsize_y, n - object.coordinate_y - object.halfmaxsize_y) 
            ),
            mode='constant'
        ) + trace
        image.image(1 - (field/field.max()), use_column_width=True)
    # We clear elements by calling empty on them.
    progress_bar.empty()
    frame_text.empty()

if __name__ == "__main__":
    run()