# Design Plan: Table Lamp

## Overview
This project is to design a modern table lamp as per the specifications in `goals.md`. The lamp consists of a weighted base, a central stem, a socket housing, and a shade. The design is intended for CNC manufacturing from aluminum. A standard light bulb is included for reference.

## Parts

### 1. base
- **Type**: Custom (Make)
- **Description**: A heavy, circular base that provides stability for the entire lamp. It features a recess on the bottom for a rubber pad and a central threaded hole for the stem.
- **Key dimensions**: ~150mm diameter, 20mm thick.
- **Interfaces**: Connects to `stem` via an M12x1.5 threaded hole.

### 2. stem
- **Type**: Custom (Make)
- **Description**: A hollow tube that connects the base to the socket housing. The internal bore allows for the passage of the power cord.
- **Key dimensions**: ~250mm length, 15mm outer diameter.
- **Interfaces**: Connects to `base` and `socket_housing` via M12x1.5 external threads.

### 3. socket_housing
- **Type**: Custom (Make)
- **Description**: Houses a standard E26 light bulb socket and provides a mounting surface for the shade.
- **Key dimensions**: ~45mm outer diameter, 60mm height.
- **Interfaces**: Connects to `stem` via an M12x1.5 threaded hole. The `shade` rests on a flange on this part.

### 4. shade
- **Type**: Custom (Make)
- **Description**: A cylindrical or conical shade that directs and diffuses light. It sits on top of the socket housing.
- **Key dimensions**: ~120mm bottom diameter, 100mm height.
- **Interfaces**: Rests on the `socket_housing`.

### 5. bulb
- **Type**: Standard (Reference)
- **Description**: A standard A-series light bulb with an E26 screw base. This part is for reference and visualization only.
- **Key dimensions**: E26 base, ~60mm max diameter.
- **Interfaces**: Screws into the E26 socket held by the `socket_housing`.

## Interfaces
- `base` ↔ `stem`: M12x1.5 threaded connection.
- `stem` ↔ `socket_housing`: M12x1.5 threaded connection.
- `socket_housing` ↔ `shade`: Gravity-held, seated fit.

## Assembly Order
1. Manufacture `base`, `stem`, `socket_housing`, and `shade`.
2. Source standard parts: E26 socket, power cord, rubber pad, bulb.
3. Feed the power cord through the `base` and up through the `stem`.
4. Screw the `stem` into the `base`.
5. Wire the E26 socket.
6. Press-fit or fasten the socket into the `socket_housing`.
7. Screw the `socket_housing` onto the `stem`.
8. Place the `shade` onto the `socket_housing`.
9. Apply the rubber pad to the recess in the `base`.
10. Screw in the `bulb`.

## Make vs Buy
- **Make**: `base`, `stem`, `socket_housing`, `shade`.
- **Buy**: E26 socket, power cord, plug, light bulb (`bulb`), rubber pad.
