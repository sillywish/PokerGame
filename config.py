from dataclasses import dataclass

@dataclass
class FrameSize:
    frame_width: int 
    frame_height: int
    frame_bg: str
    card_frame_width: int
    card_frame_height: int
    card_frame_bg: str
    card_size: tuple[int,int]
    card_gap: int
    card_top_gap: int
    title_font: tuple
    # stock_width: int
    # stock_height: int
    
    
def percent(default:FrameSize,percent) ->FrameSize:
    frame_width = percent * default.frame_width
    frame_height = percent * default.frame_height
    card_frame_width = percent * default.card_frame_width
    card_frame_height = percent * default.card_frame_height
    card_size = tuple([int(i*percent) for i in default.card_size])
    card_gap = percent * default.card_gap
    card_top_gap = percent * default.card_top_gap
    frame_bg = default.frame_bg
    card_frame_bg = default.card_frame_bg
    title_font = (default.title_font[0], int(default.title_font[1]*percent))
    
    return FrameSize(
        frame_width = frame_width,
        frame_height = frame_height,
        frame_bg = frame_bg,
        card_frame_width = card_frame_width,
        card_frame_height = card_frame_height,
        card_frame_bg = card_frame_bg,
        card_size = card_size,
        card_gap = card_gap,
        card_top_gap = card_top_gap,
        title_font = title_font                
    )
    
DEFAULT_SIZE=FrameSize(
        frame_width = 700,
        frame_height = 270,
        frame_bg = "green",
        card_frame_width = 700,
        card_frame_height = 230,
        card_frame_bg = "green",
        card_size = (150,218),
        card_gap = 30,
        card_top_gap = 15, 
        title_font = ("courier", 15)      
    )


SM_SIZE=percent(DEFAULT_SIZE,percent=0.5)
MD_SIZE=percent(DEFAULT_SIZE,percent=0.7)
BG_SIZE=percent(DEFAULT_SIZE,percent=1.4)
MELD_SIZE=FrameSize(
        frame_width = 300,
        frame_height = 140,
        frame_bg = "green",
        card_frame_width = 300,
        card_frame_height = 120,
        card_frame_bg = "green",
        card_size = (75,109),
        card_gap = 15,
        card_top_gap = 10, 
        title_font = ("courier", 7)      
    )

RUMMY_WINDOW_WIDTH = int(DEFAULT_SIZE.frame_width*1.5)
RUMMY_WINDOW_HEIGHT = int(2*DEFAULT_SIZE.frame_height+MD_SIZE.frame_height+50)
