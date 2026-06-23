import random

class Card:
    """카드 한 장"""
    def __init__(self, suit, rank):
        self.suit = suit  # 문양 (♠, ◆, ♥, ♣)
        self.rank = rank  # 숫자/알파벳 (2~10, J, Q, K, A)

    def __str__(self):
        return f"{self.suit}{self.rank}"

class Deck:
    """카드 덱 관리"""
    def __init__(self):
        suits = ['♠', '◆', '♥', '♣']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]
        random.shuffle(self.cards)

    def draw(self):
        if not self.cards:
            return None
        return self.cards.pop()

class Player:
    """플레이어 정보"""
    def __init__(self, name, is_computer=False):
        self.name = name
        self.hand = []  # 플레이어가 들고 있는 카드 리스트
        self.is_computer = is_computer

    def show_hand(self):
        """현재 가진 카드를 문자열로 반환"""
        return ", ".join([f"[{i+1}] {card}" for i, card in enumerate(self.hand)])

    def can_play(self, top_card):
        """ 낼 수 있는 카드가 한 장이라도 있는지 확인 """
        for card in self.hand:
            if card.suit == top_card.suit or card.rank == top_card.rank:
                return True
        return False

class OneCardGame:
    """게임 흐름"""
    def __init__(self):
        self.deck = Deck()
        self.discard_pile = []  # 낸 카드들이 쌓이는 곳
        self.players = [Player("플레이어 (나)"), Player("AI", is_computer=True)]
        
        # 게임 시작 시 각각 7장씩 분배
        for _ in range(7):
            for player in self.players:
                player.hand.append(self.deck.draw())
                
        # 바닥에 첫 번째 카드 놓기
        self.top_card = self.deck.draw()
        
    def draw_card(self, player):
        """덱에서 카드를 플레이어에게 제공 (덱이 비면 바닥 카드를 재셔플)"""
        drawn = self.deck.draw()
        if not drawn:
            if self.discard_pile:
                print("\n[안내] 덱이 소진되었습니다. 낸 카드들을 다시 섞습니다.")
                self.deck.cards = self.discard_pile[:]
                random.shuffle(self.deck.cards)
                self.discard_pile = []
                drawn = self.deck.draw()
        
        if drawn:
            player.hand.append(drawn)
            return drawn
        return None

    def play_game(self):
        print("=== 원카드 시작! ===")
        turn = 0
        
        while True:
            current_player = self.players[turn % 2]
            print(f"\n" + "="*40)
            print(f"바닥에 놓인 카드: [ {self.top_card} ]")
            print(f"[{current_player.name}]의 차례입니다. (남은 카드: {len(current_player.hand)}장)")
            
            if current_player.is_computer:
                self.computer_turn(current_player)
            else:
                self.user_turn(current_player)
                
            # 승리 조건 체크
            if len(current_player.hand) == 0:
                print(f"\n[{current_player.name}]이(가) 모든 카드를 내려놓아 승리했습니다!")
                break
                
            turn += 1

    def user_turn(self, player):
        print(f"내 패: {player.show_hand()}")
        
        # 낼 수 있는 카드가 아예 없는 경우 자동 드로우 후 패스
        if not player.can_play(self.top_card):
            print("낼 수 있는 카드가 없습니다. 카드 한 장을 뽑고 턴을 넘깁니다.")
            drawn = self.draw_card(player)
            if drawn:
                print(f"뽑은 카드: {drawn}")
            return

        while True:
            try:
                choice = int(input(f"낼 카드의 번호를 입력하세요 (카드를 뽑으려면 0 입력): "))
                if choice == 0:
                    drawn = self.draw_card(player)
                    if drawn:
                        print(f"카드 한 장을 뽑았습니다: {drawn}")
                    break
                
                if 1 <= choice <= len(player.hand):
                    selected_card = player.hand[choice - 1]
                    # 문양, 숫자 일치 여부 검증
                    if selected_card.suit == self.top_card.suit or selected_card.rank == self.top_card.rank:
                        self.discard_pile.append(self.top_card)
                        self.top_card = player.hand.pop(choice - 1)
                        print(f"▶ {player.name}이(가) [ {self.top_card} ] 카드를 냈습니다.")
                        break
                    else:
                        print("❌ 바닥 카드의 문양이나 숫자와 일치해야 합니다!")
                else:
                    print("❌ 올바른 카드 번호를 선택해주세요.")
            except ValueError:
                print("❌ 숫자만 입력할 수 있습니다.")

    def computer_turn(self, player):
        playable_indices = []
        for i, card in enumerate(player.hand):
            if card.suit == self.top_card.suit or card.rank == self.top_card.rank:
                playable_indices.append(i)
                
        if playable_indices:
            # AI는 낼 수 있는 카드 중 첫 번째 카드를 자동으로 냄
            chosen_idx = playable_indices[0]
            self.discard_pile.append(self.top_card)
            self.top_card = player.hand.pop(chosen_idx)
            print(f"▶ AI가 [ {self.top_card} ] 카드를 냈습니다.")
        else:
            print("AI가 낼 카드가 없어 한 장을 뽑습니다.")
            self.draw_card(player)

if __name__ == "__main__":
    game = OneCardGame()
    game.play_game()
