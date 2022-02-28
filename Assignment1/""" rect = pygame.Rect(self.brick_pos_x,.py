""" rect = pygame.Rect(self.brick_pos_x, self.brick_pos_y, self.brick_size_x, self.brick_size_y)
            for brick_red in range(20):
                pygame.draw.rect(screen, (255, 0, 0),
                (self.brick_pos_x * 2, self.brick_pos_y, self.brick_size_x, self.brick_size_y))

        def draw_brick_green(self, screen):
            rect = pygame.Rect(self.brick_pos_x, self.brick_pos_y, self.brick_size_x, self.brick_size_y)
            for brick_green in range(20):
                pygame.draw.rect(screen, (0, 255, 0),
                (self.brick_pos_x * 2, self.brick_pos_y * 2, self.brick_size_x, self.brick_size_y))

        def draw_brick_blue(self, screen):
            rect = pygame.Rect(self.brick_pos_x, self.brick_pos_y, self.brick_size_x, self.brick_size_y)
            for brick_blue in range(20):
                pygame.draw.rect(screen, (0, 0, 255),
                (self.brick_pos_x, self.brick_pos_y * 3, self.brick_size_x, self.brick_size_y)) """