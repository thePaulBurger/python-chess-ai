#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 15:20:13 2021

@author: paul
"""

import chess
import random
import time
import string 
import chess.svg


piece_values  = { 'k':1000,
                  'q':9,
                  'r':5,
                  'b':3,
                  'n':3,
                  'p':1  }


ruy_lopez = { 1:chess.Move.from_uci('e2e4'),
            2:chess.Move.from_uci('g1f3'),
            3:chess.Move.from_uci('f1b5') }


def calculate_utility(fen,perspective):
    fen_pieces = fen.split(' ')
    pieces = fen_pieces[0]
    current_player = fen_pieces[1]
    pieces =  pieces.translate(str.maketrans('', '', string.punctuation + '1234567890'))
    white_pieces = list(filter(str.isupper, pieces))
    black_pieces = list(filter(str.islower, pieces))
    white_material = 0
    for white_piece in white_pieces:
        white_material += piece_values[white_piece.lower()] 
    black_material = 0
    for black_piece in black_pieces:
        black_material += piece_values[black_piece] 
    if perspective == 'w':
        utility = white_material - black_material
    else:
        utility = black_material -  white_material
    if chess.Board(fen).is_checkmate():
           if current_player == perspective:
               utility -= 10000
           else:
               utility += 10000 
    return utility


def min_max(fen,depth,maximising_player,alpha, beta):
    if depth == 0 or chess.Board(fen).is_game_over():
        return calculate_utility(fen,'w'),''
    
    if maximising_player:
        max_eval = -float('inf')
        for move in list(chess.Board(fen).legal_moves):
            test_board = chess.Board(fen)
            test_board.push(move)
            board_eval,_ = min_max(test_board.fen(),depth-1,False, alpha, beta)  
            if board_eval > max_eval:
                return_move = move
                max_eval = board_eval
            alpha= max(alpha, max_eval)      
            if beta<=alpha:  
              break  
        return max_eval,return_move
    else:
        min_eval = float('inf')
        for move in list(chess.Board(fen).legal_moves):
            test_board = chess.Board(fen)
            test_board.push(move)
            board_eval,_ = min_max(test_board.fen(),depth-1,True, alpha, beta)
            if board_eval < min_eval:
                return_move = move
                min_eval = board_eval
            beta= min(beta, board_eval)  
            if beta<=alpha : 
                break              
        return min_eval,return_move       


def white_decision_function(fen_string):
    fen_pieces = fen_string.split(' ')
    full_move_count = fen_pieces[-1]
    if full_move_count in ruy_lopez:
        return ruy_lopez[full_move_count]
    else:
        utility,move = min_max(fen_string,3,True,-float('inf'),float('inf'))
        return move


def black_decision_function(fen_string):
    legal_moves = list(chess.Board(fen_string).legal_moves)
    selected_move = random.choice(legal_moves)
    return selected_move



class Player:
    def __init__(self, decision_function, allowed_time):
        self.time_left = allowed_time
        self.decision_function = decision_function
  
    def get_move(self,fen_string):
        start_time = time.time()
        move = self.decision_function(fen_string)
        end_time = time.time()
        self.time_left -= (end_time-start_time)  
        return move


class Game:
    def __init__(self,white_player,black_player):
        self.current_player = 'white'
        self.board = chess.Board()
        self.player_dict = {'white':white_player,'black':black_player}
        self.winner = None
        self.game_history = []
        
    def set_game_result(self):
        if (self.board.is_game_over()):
            if (self.board.is_checkmate()):
                self.winner = self.current_player
            if self.board.is_stalemate():
                self.winner = 'stalemate'
            if self.board.is_insufficient_material():
                self.winner = 'insufficient material'
            if self.board.is_fivefold_repetition():
                self.winner = 'fivefold repetition'
            if self.board.is_seventyfive_moves():
                self.winner = 'seventy five moves'
            if self.player_dict['white'].time_left <= 0 :
                self.winner == 'black'
            if self.player_dict['black'].time_left <= 0 :
                self.winner == 'white'
                

    def print_winner(self):
        if (self.winner == 'draw'):
            print('Game was a draw')
        else:
            print('{} won the game'.format(self.winner))
        
    def determine_winner(self):
        while (self.winner == None):
            # Get Game Info
            fen_string = self.board.fen()
            # Get Player Move based on current Player
            move = self.player_dict[self.current_player].get_move(fen_string)
            print('{} moved'.format(self.current_player))
            # Make Move
            self.board.push(move) 
            #Save History 
            self.game_history.append(self.board.fen())
            # Check for winner, time-out, draw etc...
            self.set_game_result()
            # Change Player
            self.current_player = 'black' if self.current_player == 'white' else 'white'
            
    def play(self):
        while (self.winner == None):
            # Get Game Info
            fen_string = self.board.fen()
            # Get Player Move based on current Player
            move = self.player_dict[self.current_player].get_move(fen_string)
            print('{} moved'.format(self.current_player))
            # Make Move
            self.board.push(move) 
            #Save History 
            self.game_history.append(self.board.fen())
            # Check for winner, time-out, draw etc...
            self.set_game_result()
            # Change Player
            self.current_player = 'black' if self.current_player == 'white' else 'white'
 
            
 
    

white_player = Player(white_decision_function,3*60)
black_player = Player(black_decision_function,3*60)
current_game = Game(white_player,black_player)
current_game.play()
current_game.print_winner()









          
    
                
                
                
                