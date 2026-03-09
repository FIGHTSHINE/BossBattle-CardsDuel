"""Boss widget canvas renderer."""

from kivy.graphics import Color, Ellipse, Line, Triangle


class BossRenderer:
    """Handles canvas drawing for boss widget."""
    
    def __init__(self, boss_widget):
        """
        Initialize renderer.
        
        Args:
            boss_widget: Parent BossWidget instance
        """
        self.widget = boss_widget
        self.canvas_instructions = {}
    
    def init_canvas(self):
        """Initialize all canvas instructions."""
        with self.widget.canvas:
            # Background aura
            self.canvas_instructions['aura_color'] = Color(1, 0.3, 0.3, 0.2)
            self.canvas_instructions['aura'] = Ellipse(pos=self.widget.pos, size=self.widget.size)
            
            # Boss body
            self.canvas_instructions['body_color'] = Color(0.9, 0.2, 0.2, 1)
            self.canvas_instructions['body'] = Ellipse(pos=self.widget.pos, size=self.widget.size)
            
            # Eyes
            self.canvas_instructions['left_eye_color'] = Color(1, 1, 0, 1)
            self.canvas_instructions['left_eye'] = Ellipse(pos=(0, 0), size=(20, 20))
            
            self.canvas_instructions['right_eye_color'] = Color(1, 1, 0, 1)
            self.canvas_instructions['right_eye'] = Ellipse(pos=(0, 0), size=(20, 20))
            
            # Pupils
            self.canvas_instructions['left_pupil_color'] = Color(0, 0, 0, 1)
            self.canvas_instructions['left_pupil'] = Ellipse(pos=(0, 0), size=(8, 8))
            
            self.canvas_instructions['right_pupil_color'] = Color(0, 0, 0, 1)
            self.canvas_instructions['right_pupil'] = Ellipse(pos=(0, 0), size=(8, 8))
            
            # Horns
            self.canvas_instructions['horn_color'] = Color(1, 0.5, 0, 1)
            self.canvas_instructions['horns'] = []
            
            # Mouth
            self.canvas_instructions['mouth_color'] = Color(0.5, 0, 0, 1)
            self.canvas_instructions['mouth'] = Line(points=[], width=2)
            
            # Scars
            self.canvas_instructions['scars'] = []
            self.canvas_instructions['scar_colors'] = []
            for i in range(3):
                with self.widget.canvas:
                    color = Color(0.2, 0, 0, 1)
                    line = Line(points=[], width=2)
                    self.canvas_instructions['scar_colors'].append(color)
                    self.canvas_instructions['scars'].append(line)
    
    def update_graphics(self, state, hp_percent):
        """
        Update all graphics based on state.
        
        Args:
            state: 'normal', 'damaged', or 'critical'
            hp_percent: Current HP percentage
        """
        center_x = self.widget.x + self.widget.width / 2
        center_y = self.widget.y + self.widget.height / 2
        radius = min(self.widget.width, self.widget.height) / 2
        
        # Update aura
        self._update_aura(state)
        
        # Update body
        self._update_body(state)
        
        # Update eyes
        self._update_eyes(center_x, center_y, radius, state)
        
        # Update horns
        self._update_horns(center_x, center_y, radius)
        
        # Update mouth
        self._update_mouth(state, center_x, center_y, radius)
        
        # Update scars
        self._update_scars(state, center_x, center_y, radius)
    
    def _update_aura(self, state):
        """Update aura based on state."""
        aura_size = (self.widget.width * 1.3, self.widget.height * 1.3)
        aura_pos = (self.widget.x - (aura_size[0] - self.widget.width) / 2,
                    self.widget.y - (aura_size[1] - self.widget.height) / 2)
        
        self.canvas_instructions['aura'].pos = aura_pos
        self.canvas_instructions['aura'].size = aura_size
        
        if state == 'normal':
            self.canvas_instructions['aura_color'].rgba = (1, 0.3, 0.3, 0.3)
        elif state == 'damaged':
            self.canvas_instructions['aura_color'].rgba = (0.7, 0.2, 0.2, 0.4)
        else:  # critical
            self.canvas_instructions['aura_color'].rgba = (0.8, 0, 0.8, 0.5)
    
    def _update_body(self, state):
        """Update body color based on state."""
        self.canvas_instructions['body'].pos = self.widget.pos
        self.canvas_instructions['body'].size = self.widget.size
        
        if state == 'normal':
            self.canvas_instructions['body_color'].rgba = (0.9, 0.2, 0.2, 1)
        elif state == 'damaged':
            self.canvas_instructions['body_color'].rgba = (0.6, 0.1, 0.1, 1)
        else:  # critical
            self.canvas_instructions['body_color'].rgba = (0.5, 0, 0.5, 1)
    
    def _update_eyes(self, center_x, center_y, radius, state):
        """Update eye positions and colors."""
        eye_offset_x = radius * 0.4
        eye_offset_y = radius * 0.2
        eye_size = radius * 0.4
        pupil_size = eye_size * 0.4
        
        # Set eye colors based on state
        if state == 'normal':
            eye_color = (1, 1, 0, 1)
        elif state == 'damaged':
            eye_color = (1, 0, 0, 1)
        else:  # critical
            eye_color = (1, 1, 1, 1)
        
        self.canvas_instructions['left_eye_color'].rgba = eye_color
        self.canvas_instructions['right_eye_color'].rgba = eye_color
        
        # Update positions
        self.canvas_instructions['left_eye'].pos = (
            center_x - eye_offset_x - eye_size/2,
            center_y + eye_offset_y - eye_size/2
        )
        self.canvas_instructions['left_eye'].size = (eye_size, eye_size)
        
        self.canvas_instructions['right_eye'].pos = (
            center_x + eye_offset_x - eye_size/2,
            center_y + eye_offset_y - eye_size/2
        )
        self.canvas_instructions['right_eye'].size = (eye_size, eye_size)
        
        self.canvas_instructions['left_pupil'].pos = (
            center_x - eye_offset_x - pupil_size/2,
            center_y + eye_offset_y - pupil_size/2
        )
        self.canvas_instructions['left_pupil'].size = (pupil_size, pupil_size)
        
        self.canvas_instructions['right_pupil'].pos = (
            center_x + eye_offset_x - pupil_size/2,
            center_y + eye_offset_y - pupil_size/2
        )
        self.canvas_instructions['right_pupil'].size = (pupil_size, pupil_size)
    
    def _update_horns(self, center_x, center_y, radius):
        """Update horn positions."""
        # Clear old horns
        for horn in self.canvas_instructions['horns']:
            self.widget.canvas.remove(horn)
        self.canvas_instructions['horns'] = []
        
        # Calculate horn positions
        left_horn_base = (center_x - radius * 0.3, center_y + radius * 0.6)
        left_horn_tip = (center_x - radius * 0.5, center_y + radius * 1.2)
        left_horn_right = (center_x - radius * 0.1, center_y + radius * 0.6)
        
        right_horn_base = (center_x + radius * 0.3, center_y + radius * 0.6)
        right_horn_tip = (center_x + radius * 0.5, center_y + radius * 1.2)
        right_horn_left = (center_x + radius * 0.1, center_y + radius * 0.6)
        
        # Create new horns
        with self.widget.canvas:
            self.canvas_instructions['horn_color'].rgba = self.canvas_instructions['horn_color'].rgba
            left_horn = Triangle(points=[
                left_horn_base[0], left_horn_base[1],
                left_horn_tip[0], left_horn_tip[1],
                left_horn_right[0], left_horn_right[1]
            ])
            self.canvas_instructions['horns'].append(left_horn)
            
            right_horn = Triangle(points=[
                right_horn_left[0], right_horn_left[1],
                right_horn_tip[0], right_horn_tip[1],
                right_horn_base[0], right_horn_base[1]
            ])
            self.canvas_instructions['horns'].append(right_horn)
    
    def _update_mouth(self, state, center_x, center_y, radius):
        """Update mouth based on state."""
        mouth_width = radius * 0.6
        mouth_y = center_y - radius * 0.2
        
        if state == 'normal':
            points = [
                center_x - mouth_width/2, mouth_y,
                center_x, mouth_y + 5,
                center_x + mouth_width/2, mouth_y
            ]
        elif state == 'damaged':
            points = [
                center_x - mouth_width/2, mouth_y,
                center_x - mouth_width/4, mouth_y - 5,
                center_x, mouth_y,
                center_x + mouth_width/4, mouth_y - 5,
                center_x + mouth_width/2, mouth_y
            ]
        else:  # critical
            points = [
                center_x - mouth_width/2, mouth_y,
                center_x - mouth_width/3, mouth_y + 10,
                center_x, mouth_y + 15,
                center_x + mouth_width/3, mouth_y + 10,
                center_x + mouth_width/2, mouth_y
            ]
        
        self.canvas_instructions['mouth'].points = points
    
    def _update_scars(self, state, center_x, center_y, radius):
        """Update battle scars."""
        if state == 'normal':
            for scar in self.canvas_instructions['scars']:
                scar.points = []
        else:
            scar_positions = [
                [(center_x - radius * 0.5, center_y + radius * 0.2),
                 (center_x - radius * 0.2, center_y - radius * 0.1)],
                [(center_x + radius * 0.3, center_y + radius * 0.3),
                 (center_x + radius * 0.3, center_y - radius * 0.2)],
                [(center_x - radius * 0.1, center_y - radius * 0.3),
                 (center_x + radius * 0.2, center_y - radius * 0.4)]
            ]
            
            for i, scar in enumerate(self.canvas_instructions['scars']):
                if i < len(scar_positions):
                    scar.points = [coord for point in scar_positions[i] for coord in point]
                    if state == 'damaged':
                        self.canvas_instructions['scar_colors'][i].rgba = (0.2, 0, 0, 1)
                    else:  # critical
                        self.canvas_instructions['scar_colors'][i].rgba = (0.5, 0, 0.5, 1)