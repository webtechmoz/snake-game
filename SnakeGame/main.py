import flet as ft
from random import randrange
import asyncio

class squad(ft.Container):
    def __init__(
        self,
        top: float = None,
        left: float = None,
        bgcolor: ft.colors = None,
        width: float = 12,
        height: float = 12,
        border_radius: float = None
    ):
        super().__init__()
        self.top = top
        self.left = left
        self.border_radius = border_radius
        self.bgcolor = bgcolor
        self.width = width
        self.height = height

class Snake(squad):
    def __init__(
        self,
        top: float = 12,
        left: float = 20
    ):
        super().__init__()
        self.top = top
        self.left = left
        self.bgcolor = ft.colors.WHITE
        self.border_radius = 1

class Eat(squad):
    def __init__(
        self,
        top: float = randrange(1, 387),
        left: float = randrange(1, 387),
        width: float = 15,
        height: float = 15
    ):
        super().__init__()
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        self.border_radius = width
        self.bgcolor = ft.colors.BLUE

class Pontuation(ft.Row):
    def __init__(
        self,
        value: int = 0
    ):
        self.color = ft.colors.with_opacity(0.6, 'green')
        super().__init__()
        self.controls = [
            ft.Icon(
                name=ft.icons.SCORE,
                size=14,
                color=self.color
            ),
            ft.Text(
                value='Score:'.upper(),
                size=12,
                weight='bold',
                color=self.color
            ),
            ft.Text(
                value=value,
                size=12,
                weight='bold',
                color=self.color
            )
        ]
        self.spacing = 2
        self.alignment = ft.MainAxisAlignment.END

class SpaceGame(ft.Container):
    def __init__(
        self
    ):
        super().__init__()
        self.width = 400
        self.height = 400
        self.border_radius = 2
        self.padding = ft.padding.all(1)
        self.bgcolor = ft.colors.BLACK
        self.content = ft.Stack(
            controls=[
                ft.Stack(
                    controls=[
                        Snake()
                    ]
                ),
                Pontuation(),
                Eat()
            ],
            width=self.width,
            height=self.height
        )

def main(page: ft.Page):
    page.title = 'Jogo da Cobrinha'

    # Logica do jogo
    class Playing():
        def __init__(self):
            self.diretion = 'right'
        
        def key_pressed(self, e: ft.KeyboardEvent):
            if e.key == 'Arrow Up' and self.diretion in ['right', 'left']:
                self.diretion = 'up'
            
            elif e.key == 'Arrow Down' and self.diretion in ['right', 'left']:
                self.diretion = 'down'
            
            elif e.key == 'Arrow Left' and self.diretion in ['up', 'down']:
                self.diretion = 'left'
            
            elif e.key == 'Arrow Right' and self.diretion in ['up', 'down']:
                self.diretion = 'right'
        
        def snake_eat(self, snake_head: Snake, eat: Eat):
            points = eat.parent.controls[1].controls[-1]

            if abs(snake_head.left - eat.left) < 12 and abs(snake_head.top - eat.top) < 12:
                top, left = [randrange(1, 384) for _ in range(2)]
                eat.parent.controls.remove(eat)
                points.value = int(points.value) + 5

                eat.parent.controls.append(
                    Eat(
                        top=top,
                        left=left
                    )
                )
                snake_head.parent.controls.append(
                    Snake(
                        top=snake_head.parent.controls[-1].top,
                        left=snake_head.parent.controls[-1].left
                    )
                )
        
        async def snake_move(self):
            while True:
                try:
                    snake_body: list[Snake] = page.views[-1].controls[0].content.controls[0].controls
                    snake_head = snake_body[0]
                    eat: Eat = page.views[-1].controls[0].content.controls[-1]

                    for i in range(len(snake_body)-1, 0, -1):
                        snake_body[i].left = snake_body[i-1].left
                        snake_body[i].top = snake_body[i-1].top
                    
                    if self.diretion == 'right':
                        if snake_head.left < 387:
                            snake_head.left += 1
                        
                        else:
                            snake_head.left = 1
                    
                    elif self.diretion == 'left':
                        if snake_head.left > 0:
                            snake_head.left -= 1
                        
                        else:
                            snake_head.left = 399
                    
                    elif self.diretion == 'up':
                        if snake_head.top > 0:
                            snake_head.top -= 1
                        
                        else:
                            snake_head.top = 399
                    
                    elif self.diretion == 'down':
                        if snake_head.top < 387:
                            snake_head.top += 1
                        
                        else:
                            snake_head.top = 1
                    
                    self.snake_eat(snake_head, eat)
                except:
                    pass
                
                page.update()
                await asyncio.sleep(0.01)

    def router(route):
        page.views.clear()

        if page.route == '/':
            page.views.append(
                ft.View(
                    route='/',
                    controls=[
                        SpaceGame()
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )

            page.update()
    
    play = Playing()
    page.on_route_change = router
    page.go(page.route)

    page.on_keyboard_event = play.key_pressed
    asyncio.run(play.snake_move())

if __name__ == '__main__':
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)