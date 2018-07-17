#include <iostream>
#include <vector>
#include <SDL.h>
#include <SDL_image.h>

const int SCREEN_WIDTH = 640;
const int SCREEN_HEIGHT = 480;

const int GAME_SPEED = 50;

SDL_Window *window = NULL;
SDL_Renderer *renderer = NULL;
SDL_Event event;
SDL_Surface* bg = NULL;
SDL_Texture* texture = NULL;

void Init() {
	SDL_Init(SDL_INIT_VIDEO);
	window = SDL_CreateWindow("Risiko", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED,
		SCREEN_WIDTH, SCREEN_HEIGHT, SDL_WINDOW_SHOWN);
	renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
	SDL_SetRenderDrawColor(renderer, 0xFF, 0xFF, 0xFF, 0xFF);
	SDL_RenderClear(renderer);

	bg = SDL_LoadBMP("bg.bmp");
	texture = SDL_CreateTextureFromSurface(renderer, bg);
}

void close() {
	SDL_FreeSurface(bg);
	bg = NULL;
	SDL_DestroyTexture(texture);
	texture = NULL;
	SDL_DestroyRenderer(renderer);
	SDL_DestroyWindow(window);
	window = NULL;
	SDL_Quit();
}

void drawBackground() {
	SDL_RenderCopy(renderer, texture, NULL, NULL);
	SDL_RenderPresent(renderer);
}

int main(int argc, char* args[]) {
	Init();
	bool quit = false;

	while (!quit) {
		while (SDL_PollEvent(&event) != 0)
			if (event.type == SDL_QUIT)
				quit = true;
		SDL_SetRenderDrawColor(renderer, 0xFF, 0xFF, 0xFF, 0xFF);
		SDL_RenderClear(renderer);

		drawBackground();

		SDL_RenderPresent(renderer);
		SDL_Delay(GAME_SPEED);
	}

	close();
	return 0;
}