import math
import tkinter as tk
from collections import deque
from dataclasses import dataclass, field
from tkinter import messagebox


CITY_NODES = {
    "Johannesburg",
    "Cape Town",
    "Durban",
    "Gqeberha",
    "Polokwane",
    "Mbombela",
    "Bloemfontein",
    "Rustenburg",
    "Kimberley",
}

PROVINCE_COLORS = {
    "Western Cape": "#d9f0ff",
    "Northern Cape": "#fce4c3",
    "Eastern Cape": "#d9ead3",
    "KwaZulu-Natal": "#f4cccc",
    "Free State": "#fff2cc",
    "North West": "#ead1dc",
    "Gauteng": "#d0e0e3",
    "Limpopo": "#f9cb9c",
    "Mpumalanga": "#cfe2f3",
}

POLICE_ROUTES = {
    frozenset(("Worcester", "Kimberley")),
    frozenset(("Kimberley", "Bloemfontein")),
    frozenset(("Bloemfontein", "Durban")),
    frozenset(("Ladysmith", "Newcastle")),
    frozenset(("Brits", "Johannesburg")),
    frozenset(("Mbombela", "White River")),
}

NODE_DATA = [
    ("Cape Town", "Western Cape", 29, 110, 570),
    ("Stellenbosch", "Western Cape", 13, 180, 545),
    ("Paarl", "Western Cape", 10, 210, 515),
    ("Worcester", "Western Cape", 5, 285, 490),
    ("George", "Western Cape", 7, 260, 615),
    ("Kimberley", "Northern Cape", 20, 390, 360),
    ("Upington", "Northern Cape", 8, 225, 320),
    ("Springbok", "Northern Cape", 5, 120, 250),
    ("De Aar", "Northern Cape", 3, 355, 445),
    ("Postmasburg", "Northern Cape", 7, 330, 300),
    ("Bloemfontein", "Free State", 25, 520, 405),
    ("Welkom", "Free State", 10, 515, 335),
    ("Sasolburg", "Free State", 7, 580, 290),
    ("Kroonstad", "Free State", 5, 565, 345),
    ("Phuthaditjhaba", "Free State", 9, 630, 375),
    ("Rustenburg", "North West", 23, 560, 205),
    ("Klerksdorp", "North West", 14, 475, 250),
    ("Mahikeng", "North West", 9, 430, 180),
    ("Brits", "North West", 6, 610, 180),
    ("Potchefstroom", "North West", 11, 520, 255),
    ("Johannesburg", "Gauteng", 27, 705, 240),
    ("Soweto", "Gauteng", 11, 675, 275),
    ("Benoni", "Gauteng", 8, 760, 235),
    ("Germiston", "Gauteng", 14, 735, 265),
    ("Kempton Park", "Gauteng", 9, 760, 205),
    ("Polokwane", "Limpopo", 22, 720, 90),
    ("Tzaneen", "Limpopo", 10, 790, 85),
    ("Bela-Bela", "Limpopo", 6, 675, 145),
    ("Mokopane", "Limpopo", 9, 745, 135),
    ("Louis Trichardt", "Limpopo", 5, 760, 40),
    ("Mbombela", "Mpumalanga", 21, 860, 220),
    ("Witbank/eMalahleni", "Mpumalanga", 12, 800, 200),
    ("Middelburg", "Mpumalanga", 8, 835, 180),
    ("Secunda", "Mpumalanga", 11, 790, 265),
    ("White River", "Mpumalanga", 4, 900, 200),
    ("Durban", "KwaZulu-Natal", 26, 820, 405),
    ("Pietermaritzburg", "KwaZulu-Natal", 12, 760, 360),
    ("Richards Bay", "KwaZulu-Natal", 9, 860, 330),
    ("Ladysmith", "KwaZulu-Natal", 6, 720, 320),
    ("Newcastle", "KwaZulu-Natal", 11, 765, 270),
    ("Gqeberha", "Eastern Cape", 24, 665, 555),
    ("East London", "Eastern Cape", 15, 720, 505),
    ("Mthatha", "Eastern Cape", 8, 755, 455),
    ("Grahamstown", "Eastern Cape", 4, 640, 585),
    ("Queenstown", "Eastern Cape", 7, 650, 470),
]

EDGE_LIST = [
    ("Cape Town", "Stellenbosch"),
    ("Cape Town", "Paarl"),
    ("Stellenbosch", "Paarl"),
    ("Paarl", "Worcester"),
    ("Worcester", "George"),
    ("Worcester", "De Aar"),
    ("Worcester", "Kimberley"),
    ("George", "Gqeberha"),
    ("Kimberley", "Upington"),
    ("Upington", "Springbok"),
    ("Kimberley", "Postmasburg"),
    ("Kimberley", "De Aar"),
    ("Kimberley", "Bloemfontein"),
    ("Postmasburg", "Mahikeng"),
    ("De Aar", "Bloemfontein"),
    ("Bloemfontein", "Welkom"),
    ("Welkom", "Kroonstad"),
    ("Kroonstad", "Sasolburg"),
    ("Bloemfontein", "Phuthaditjhaba"),
    ("Phuthaditjhaba", "Ladysmith"),
    ("Bloemfontein", "Queenstown"),
    ("Queenstown", "East London"),
    ("Queenstown", "Mthatha"),
    ("Gqeberha", "Grahamstown"),
    ("Grahamstown", "East London"),
    ("East London", "Mthatha"),
    ("Gqeberha", "Queenstown"),
    ("Mthatha", "Durban"),
    ("Durban", "Pietermaritzburg"),
    ("Pietermaritzburg", "Ladysmith"),
    ("Ladysmith", "Newcastle"),
    ("Durban", "Richards Bay"),
    ("Richards Bay", "Newcastle"),
    ("Newcastle", "Secunda"),
    ("Secunda", "Witbank/eMalahleni"),
    ("Witbank/eMalahleni", "Middelburg"),
    ("Middelburg", "Mbombela"),
    ("Mbombela", "White River"),
    ("Witbank/eMalahleni", "Johannesburg"),
    ("Secunda", "Johannesburg"),
    ("Sasolburg", "Johannesburg"),
    ("Johannesburg", "Germiston"),
    ("Johannesburg", "Soweto"),
    ("Johannesburg", "Benoni"),
    ("Johannesburg", "Kempton Park"),
    ("Germiston", "Benoni"),
    ("Germiston", "Kempton Park"),
    ("Benoni", "Kempton Park"),
    ("Johannesburg", "Brits"),
    ("Brits", "Rustenburg"),
    ("Rustenburg", "Mahikeng"),
    ("Rustenburg", "Klerksdorp"),
    ("Klerksdorp", "Potchefstroom"),
    ("Potchefstroom", "Johannesburg"),
    ("Klerksdorp", "Welkom"),
    ("Brits", "Bela-Bela"),
    ("Bela-Bela", "Polokwane"),
    ("Polokwane", "Mokopane"),
    ("Polokwane", "Tzaneen"),
    ("Polokwane", "Louis Trichardt"),
    ("Mokopane", "Bela-Bela"),
    ("Mokopane", "Witbank/eMalahleni"),
    ("Tzaneen", "Mbombela"),
    ("Polokwane", "Mbombela"),
]


@dataclass
class Node:
    name: str
    province: str
    points: int
    x: int
    y: int
    is_city: bool = False


@dataclass
class Player:
    name: str
    color: str
    position: str = "Cape Town"
    score: int = 149
    skip_turns: int = 0
    visited: set = field(default_factory=lambda: {"Cape Town"})
    toll_paid_cities: set = field(default_factory=lambda: {"Cape Town"})


class AgeOfWheelsGame:
    def __init__(self):
        self.nodes = {
            name: Node(
                name=name,
                province=province,
                points=points,
                x=x,
                y=y,
                is_city=name in CITY_NODES,
            )
            for name, province, points, x, y in NODE_DATA
        }
        self.adjacency = {name: set() for name in self.nodes}
        for left, right in EDGE_LIST:
            self.adjacency[left].add(right)
            self.adjacency[right].add(left)

        self.players = [
            Player(name="Player 1", color="#d64550"),
            Player(name="Player 2", color="#2b6cb0"),
        ]
        self.current_player_index = 0
        self.turn_number = 1
        self.turn_invested = False
        self.claimed_nodes = {"Cape Town"}
        self.route_owners = {}
        self.pending_police_move = None
        self.winner = None

    @property
    def current_player(self):
        return self.players[self.current_player_index]

    @property
    def opponent(self):
        return self.players[1 - self.current_player_index]

    def route_key(self, left, right):
        return tuple(sorted((left, right)))

    def get_accessible_neighbors(self, player):
        options = []
        for neighbor in sorted(self.adjacency[player.position]):
            edge = self.route_key(player.position, neighbor)
            owner = self.route_owners.get(edge)
            toll = self.get_toll_cost(player, player.position, neighbor)
            access_fee = 15 if owner is not None and owner != player.name else 0
            total_required = access_fee + (toll or 0)
            if player.score < total_required:
                continue
            options.append(neighbor)
        return options

    def get_toll_cost(self, player, start, destination):
        owner = self.route_owners.get(self.route_key(start, destination))
        if owner == player.name:
            return None
        dest_node = self.nodes[destination]
        start_node = self.nodes[start]
        if (
            dest_node.is_city
            and dest_node.province != start_node.province
            and destination not in player.toll_paid_cities
        ):
            return math.ceil(dest_node.points / 2)
        return None

    def get_available_investments(self, player):
        distance_map = self.bfs_distances(player.position)
        offers = []
        for start, distance in distance_map.items():
            if distance != 2:
                continue
            for destination in sorted(self.adjacency[start]):
                edge = self.route_key(start, destination)
                if edge in self.route_owners:
                    continue
                cost = self.nodes[destination].points
                if player.score < cost:
                    continue
                offers.append((start, destination, cost))
        offers.sort(key=lambda item: (item[2], item[0], item[1]))
        return offers

    def bfs_distances(self, origin):
        distances = {origin: 0}
        queue = deque([origin])
        while queue:
            current = queue.popleft()
            for neighbor in self.adjacency[current]:
                if neighbor in distances:
                    continue
                distances[neighbor] = distances[current] + 1
                queue.append(neighbor)
        return distances

    def invest_in_route(self, start, destination):
        if self.winner:
            return False, "The game is already finished."
        if self.turn_invested:
            return False, "You already invested once this turn."
        player = self.current_player
        edge = self.route_key(start, destination)
        if edge in self.route_owners:
            return False, "That route is already owned."
        if not any(
            offer[0] == start and offer[1] == destination
            for offer in self.get_available_investments(player)
        ):
            return False, "That road is not a valid investment from your current position."
        cost = self.nodes[destination].points
        player.score -= cost
        self.route_owners[edge] = player.name
        self.turn_invested = True
        return True, f"{player.name} invested in {start} - {destination} for {cost} points."

    def move_current_player(self, destination, police_choice=None):
        if self.winner:
            return False, "The game is already finished."

        player = self.current_player
        if player.skip_turns > 0:
            return False, f"{player.name} must skip this turn."
        if destination not in self.adjacency[player.position]:
            return False, "You can only move to an adjacent node."

        edge = self.route_key(player.position, destination)
        owner = self.route_owners.get(edge)
        toll_cost = self.get_toll_cost(player, player.position, destination)
        access_fee = 15 if owner is not None and owner != player.name else 0
        if player.score < access_fee:
            return False, "You cannot afford the 15-point owner access fee for that road."
        if toll_cost is not None and player.score < access_fee + toll_cost:
            return False, "You cannot afford the provincial city toll on that move."

        if frozenset((player.position, destination)) in POLICE_ROUTES and owner != player.name:
            if police_choice not in {"bribe", "refuse"}:
                self.pending_police_move = {
                    "player": player.name,
                    "from": player.position,
                    "to": destination,
                }
                return False, f"Police encounter on {player.position} - {destination}. Choose bribe or refuse."
            if police_choice == "bribe":
                total_cost = access_fee + (toll_cost or 0) + 15
                if player.score < total_cost:
                    return False, "You cannot afford the police bribe."
                player.score -= 15
                police_message = " Bribed the police for 15 points."
            else:
                player.skip_turns = 1
                police_message = " Refused the police and will lose the next turn."
        else:
            police_message = ""

        transfer_message = ""
        if access_fee:
            player.score -= access_fee
            self.player_by_name(owner).score += access_fee
            transfer_message = f" Paid 15 points to {owner} to use the owned road."

        toll_message = ""
        if toll_cost is not None:
            player.score -= toll_cost
            player.toll_paid_cities.add(destination)
            toll_message = f" Toll paid: {toll_cost} points."

        self.pending_police_move = None
        player.position = destination
        reward_message = ""
        if destination not in self.claimed_nodes:
            self.claimed_nodes.add(destination)
            player.visited.add(destination)
            player.score += self.nodes[destination].points
            reward_message = f" Claimed {self.nodes[destination].points} points from {destination}."
        self.check_winner(player)
        return True, (
            f"{player.name} moved to {destination}."
            f"{toll_message}{transfer_message}{police_message}{reward_message}"
        )

    def player_by_name(self, name):
        return next(player for player in self.players if player.name == name)

    def end_turn(self):
        if self.winner:
            return f"{self.winner.name} has already won."
        self.current_player_index = 1 - self.current_player_index
        self.turn_number += 1
        self.turn_invested = False
        player = self.current_player
        if player.skip_turns > 0:
            player.skip_turns -= 1
            skipped_name = player.name
            self.current_player_index = 1 - self.current_player_index
            self.turn_number += 1
            self.turn_invested = False
            return f"{skipped_name} lost this turn after refusing the police stop."
        return f"It is now {player.name}'s turn."

    def check_winner(self, player):
        if player.position == "Johannesburg" and player.score >= 200:
            self.winner = player


class GameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Age of Wheels: South Africa")
        self.root.geometry("1330x760")
        self.root.configure(bg="#f6f2e8")

        self.game = AgeOfWheelsGame()
        self.node_items = {}
        self.marker_items = {}
        self.edge_items = {}
        self.selected_node = None
        self.investment_map = {}

        self.build_layout()
        self.draw_board()
        self.refresh_ui()
        self.log(
            "Both players begin at Cape Town with 120 starting points plus the Cape Town reward (149 total). "
            "Reach Johannesburg with at least 200 points to win."
        )

    def build_layout(self):
        main = tk.Frame(self.root, bg="#f6f2e8")
        main.pack(fill="both", expand=True, padx=12, pady=12)

        self.canvas = tk.Canvas(
            main,
            width=980,
            height=720,
            bg="#fcfaf4",
            highlightthickness=0,
        )
        self.canvas.pack(side="left", fill="both", expand=False)

        sidebar = tk.Frame(main, bg="#f6f2e8", width=320)
        sidebar.pack(side="right", fill="both", expand=True, padx=(14, 0))

        title = tk.Label(
            sidebar,
            text="Age of Wheels: South Africa",
            font=("Helvetica", 18, "bold"),
            bg="#f6f2e8",
            anchor="w",
        )
        title.pack(fill="x")

        subtitle = tk.Label(
            sidebar,
            text="Two-player route strategy race to Johannesburg",
            font=("Helvetica", 10),
            fg="#555555",
            bg="#f6f2e8",
            anchor="w",
        )
        subtitle.pack(fill="x", pady=(0, 10))

        self.turn_var = tk.StringVar()
        self.turn_label = tk.Label(
            sidebar,
            textvariable=self.turn_var,
            font=("Helvetica", 12, "bold"),
            justify="left",
            bg="#e8efe5",
            padx=10,
            pady=8,
            anchor="w",
        )
        self.turn_label.pack(fill="x", pady=(0, 10))

        self.player_panels = []
        for index in range(2):
            frame = tk.Frame(sidebar, bg="#ffffff", bd=1, relief="solid")
            frame.pack(fill="x", pady=(0, 8))
            label = tk.Label(frame, justify="left", anchor="w", bg="#ffffff", padx=10, pady=8)
            label.pack(fill="x")
            self.player_panels.append(label)

        move_frame = tk.LabelFrame(sidebar, text="Movement", bg="#f6f2e8", padx=8, pady=8)
        move_frame.pack(fill="x", pady=(8, 8))
        self.move_hint_var = tk.StringVar()
        tk.Label(
            move_frame,
            textvariable=self.move_hint_var,
            justify="left",
            anchor="w",
            bg="#f6f2e8",
            wraplength=280,
        ).pack(fill="x")

        police_frame = tk.LabelFrame(sidebar, text="Police Decision", bg="#f6f2e8", padx=8, pady=8)
        police_frame.pack(fill="x", pady=(0, 8))
        self.police_var = tk.StringVar(value="No active police stop.")
        tk.Label(
            police_frame,
            textvariable=self.police_var,
            justify="left",
            anchor="w",
            bg="#f6f2e8",
            wraplength=280,
        ).pack(fill="x")
        police_button_row = tk.Frame(police_frame, bg="#f6f2e8")
        police_button_row.pack(fill="x", pady=(6, 0))
        self.bribe_button = tk.Button(police_button_row, text="Bribe (15)", command=lambda: self.resolve_police("bribe"))
        self.bribe_button.pack(side="left", padx=(0, 6))
        self.refuse_button = tk.Button(police_button_row, text="Refuse", command=lambda: self.resolve_police("refuse"))
        self.refuse_button.pack(side="left")

        invest_frame = tk.LabelFrame(sidebar, text="Invest In Road 2 Ahead", bg="#f6f2e8", padx=8, pady=8)
        invest_frame.pack(fill="x", pady=(0, 8))
        self.invest_listbox = tk.Listbox(invest_frame, height=8)
        self.invest_listbox.pack(fill="x")
        self.invest_button = tk.Button(invest_frame, text="Invest In Selected Road", command=self.invest_selected)
        self.invest_button.pack(fill="x", pady=(6, 0))

        controls = tk.Frame(sidebar, bg="#f6f2e8")
        controls.pack(fill="x", pady=(2, 8))
        self.end_turn_button = tk.Button(controls, text="End Turn", command=self.end_turn)
        self.end_turn_button.pack(fill="x")

        log_frame = tk.LabelFrame(sidebar, text="Game Log", bg="#f6f2e8", padx=8, pady=8)
        log_frame.pack(fill="both", expand=True)
        self.log_text = tk.Text(log_frame, height=18, wrap="word", state="disabled")
        self.log_text.pack(fill="both", expand=True)

    def draw_board(self):
        for left, right in EDGE_LIST:
            a = self.game.nodes[left]
            b = self.game.nodes[right]
            is_police = frozenset((left, right)) in POLICE_ROUTES
            color = "#b04a3f" if is_police else "#9b9b9b"
            dash = (6, 4) if is_police else None
            item = self.canvas.create_line(a.x, a.y, b.x, b.y, fill=color, width=2, dash=dash)
            self.edge_items[self.game.route_key(left, right)] = item

        for node in self.game.nodes.values():
            radius = 18 if node.is_city else 12
            fill = "#f5be3d" if node.is_city else "#ffffff"
            outline = "#3f3f3f"
            item = self.canvas.create_oval(
                node.x - radius,
                node.y - radius,
                node.x + radius,
                node.y + radius,
                fill=fill,
                outline=outline,
                width=2,
            )
            self.node_items[node.name] = item
            self.canvas.tag_bind(item, "<Button-1>", lambda _event, name=node.name: self.handle_node_click(name))
            self.canvas.create_text(
                node.x,
                node.y - (28 if node.is_city else 22),
                text=f"{node.name}\n({node.points})",
                font=("Helvetica", 8, "bold" if node.is_city else "normal"),
                justify="center",
            )

        for province, color in PROVINCE_COLORS.items():
            members = [node for node in self.game.nodes.values() if node.province == province]
            avg_x = sum(node.x for node in members) / len(members)
            avg_y = sum(node.y for node in members) / len(members)
            self.canvas.create_text(
                avg_x,
                avg_y + 32,
                text=province,
                fill=color,
                font=("Helvetica", 12, "bold"),
            )

        legend_x = 28
        legend_y = 24
        self.canvas.create_text(legend_x, legend_y, text="Legend", anchor="w", font=("Helvetica", 11, "bold"))
        self.canvas.create_line(legend_x, legend_y + 20, legend_x + 28, legend_y + 20, fill="#9b9b9b", width=2)
        self.canvas.create_text(legend_x + 35, legend_y + 20, text="Normal road", anchor="w", font=("Helvetica", 9))
        self.canvas.create_line(
            legend_x,
            legend_y + 42,
            legend_x + 28,
            legend_y + 42,
            fill="#b04a3f",
            width=2,
            dash=(6, 4),
        )
        self.canvas.create_text(legend_x + 35, legend_y + 42, text="Police route", anchor="w", font=("Helvetica", 9))
        self.canvas.create_text(
            legend_x,
            legend_y + 64,
            text="Cities trigger one-time province tolls when entered from another province.",
            anchor="w",
            width=250,
            font=("Helvetica", 9),
        )

        for index, player in enumerate(self.game.players):
            marker = self.canvas.create_oval(0, 0, 0, 0, fill=player.color, outline="#222222", width=2)
            self.marker_items[player.name] = marker
        self.reposition_markers()

    def handle_node_click(self, node_name):
        if self.game.pending_police_move is not None:
            self.log("Resolve the police stop before moving again.")
            return

        current_player = self.game.current_player
        if node_name not in self.game.get_accessible_neighbors(current_player):
            self.log(f"{node_name} is not currently available for {current_player.name}.")
            return

        success, message = self.game.move_current_player(node_name)
        self.log(message)
        self.refresh_ui()
        if success:
            self.finish_turn_if_needed()

    def resolve_police(self, choice):
        pending = self.game.pending_police_move
        if pending is None:
            self.log("There is no active police stop to resolve.")
            return
        if pending["player"] != self.game.current_player.name:
            self.log("The pending police stop no longer belongs to the active player.")
            return

        success, message = self.game.move_current_player(pending["to"], police_choice=choice)
        self.log(message)
        self.refresh_ui()
        if success:
            self.finish_turn_if_needed()

    def finish_turn_if_needed(self):
        self.refresh_ui()
        if self.game.winner:
            self.log(f"{self.game.winner.name} wins by reaching Johannesburg with {self.game.winner.score} points.")
            messagebox.showinfo("Winner", f"{self.game.winner.name} wins!")
            return
        auto_message = self.game.end_turn()
        self.log(auto_message)
        self.refresh_ui()

    def end_turn(self):
        if self.game.pending_police_move is not None:
            self.log("You need to resolve the police choice before ending the turn.")
            return
        message = self.game.end_turn()
        self.log(message)
        self.refresh_ui()

    def invest_selected(self):
        if self.game.winner:
            return
        selection = self.invest_listbox.curselection()
        if not selection:
            self.log("Choose a route from the investment list first.")
            return
        key = self.invest_listbox.get(selection[0])
        if key not in self.investment_map:
            self.log("There is no legal investment tied to that list entry.")
            return
        start, destination = self.investment_map[key]
        self.log(f"Attempting investment on {start} - {destination}.")
        success, message = self.game.invest_in_route(start, destination)
        self.log(message)
        if success:
            self.refresh_ui()

    def reposition_markers(self):
        offsets = [(-10, -10), (10, 10)]
        for index, player in enumerate(self.game.players):
            node = self.game.nodes[player.position]
            dx, dy = offsets[index]
            marker = self.marker_items[player.name]
            self.canvas.coords(marker, node.x + dx - 6, node.y + dy - 6, node.x + dx + 6, node.y + dy + 6)

    def refresh_ui(self):
        current = self.game.current_player
        self.turn_var.set(
            f"Turn {self.game.turn_number}: {current.name}\n"
            f"Current location: {current.position}\n"
            f"Target: reach Johannesburg with at least 200 points"
        )

        for label, player in zip(self.player_panels, self.game.players):
            owned_count = sum(1 for owner in self.game.route_owners.values() if owner == player.name)
            label.config(
                text=(
                    f"{player.name}\n"
                    f"Location: {player.position}\n"
                    f"Points: {player.score}\n"
                    f"Owned roads: {owned_count}\n"
                    f"Police skips queued: {player.skip_turns}"
                ),
                fg=player.color,
                font=("Helvetica", 11, "bold" if player == current else "normal"),
            )

        for name, item in self.node_items.items():
            node = self.game.nodes[name]
            if name == current.position:
                fill = "#9ad0f5"
            elif name in self.game.get_accessible_neighbors(current):
                fill = "#b7e4c7"
            elif name in self.game.claimed_nodes:
                fill = "#d6d6d6" if not node.is_city else "#d1b36a"
            else:
                fill = "#f5be3d" if node.is_city else "#ffffff"
            self.canvas.itemconfig(item, fill=fill)

        for edge, item in self.edge_items.items():
            owner = self.game.route_owners.get(edge)
            if owner == "Player 1":
                color = "#d64550"
                width = 4
                dash = None
            elif owner == "Player 2":
                color = "#2b6cb0"
                width = 4
                dash = None
            elif frozenset(edge) in POLICE_ROUTES:
                color = "#b04a3f"
                width = 2
                dash = (6, 4)
            else:
                color = "#9b9b9b"
                width = 2
                dash = None
            self.canvas.itemconfig(item, fill=color, width=width, dash=dash)

        self.reposition_markers()
        neighbors = self.game.get_accessible_neighbors(current)
        if self.game.pending_police_move:
            pending = self.game.pending_police_move
            self.move_hint_var.set(
                f"Police stop pending on {pending['from']} -> {pending['to']}. "
                "Choose Bribe or Refuse before continuing."
            )
            self.police_var.set(
                f"{current.name} is stopped between {pending['from']} and {pending['to']}. "
                "Bribe costs 15 points. Refuse means you lose your next turn."
            )
            self.bribe_button.config(state="normal")
            self.refuse_button.config(state="normal")
        else:
            if neighbors:
                self.move_hint_var.set(
                    "Click one of the highlighted neighboring nodes to move:\n" + ", ".join(neighbors)
                )
            else:
                self.move_hint_var.set("No affordable moves are available from this location.")
            self.police_var.set("No active police stop.")
            self.bribe_button.config(state="disabled")
            self.refuse_button.config(state="disabled")

        self.invest_listbox.delete(0, tk.END)
        self.investment_map.clear()
        for start, destination, cost in self.game.get_available_investments(current):
            label = f"{start} -> {destination} (cost {cost})"
            self.invest_listbox.insert(tk.END, label)
            self.investment_map[label] = (start, destination)
        if self.invest_listbox.size() == 0:
            self.invest_listbox.insert(tk.END, "No legal investments right now")
            self.invest_button.config(state="disabled")
        else:
            self.invest_button.config(state="normal")

        game_over = self.game.winner is not None
        self.end_turn_button.config(state="disabled" if game_over else "normal")
        if game_over:
            self.move_hint_var.set(f"{self.game.winner.name} has won the game.")
            self.invest_button.config(state="disabled")

    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert("end", f"{message}\n\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")


def main():
    root = tk.Tk()
    app = GameApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
