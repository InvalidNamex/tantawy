# Quantity System Documentation

## Overview

The quantity system in this application supports multi-unit item management, allowing items to be measured and sold in up to three different unit types: **Main Unit**, **Sub Unit**, and **Small Unit**. This is particularly useful for inventory and sales systems where products can be sold in different packaging sizes.

## Unit Hierarchy

The system uses a hierarchical structure where smaller units can be converted into larger units based on pack sizes:

```
Main Unit (Base)
  └─ Sub Unit (mainUnitPack)
      └─ Small Unit (subUnitPack)
```

### Unit Types

1. **Main Unit**: The primary/base unit for an item
   - Example: Box, Carton, Kilogram
   - This is the reference unit for all calculations

2. **Sub Unit** (Optional): A smaller unit contained within the main unit
   - Example: Pack, Piece, Gram
   - Converted to main unit using `mainUnitPack`

3. **Small Unit** (Optional): The smallest unit in the hierarchy
   - Example: Individual piece, Milligram
   - Converted to sub unit using `subUnitPack`, then to main unit

## Pack Sizes

Pack sizes define the conversion ratios between units:

- **`mainUnitPack`**: Number of sub units in one main unit
  - Example: If 1 Box = 12 Packs, then `mainUnitPack = 12`

- **`subUnitPack`**: Number of small units in one sub unit
  - Example: If 1 Pack = 10 Pieces, then `subUnitPack = 10`

## Quantity Conversion Formula

All quantities are converted to the main unit for consistent calculations:

### Sub Unit Conversion
```
subQtyInMainUnit = subQty / mainUnitPack
```

### Small Unit Conversion
```
smallQtyInMainUnit = (smallQty / subUnitPack) / mainUnitPack
```

### Total Quantity
```
totalQty = mainQty + subQtyInMainUnit + smallQtyInMainUnit
```

## Example Calculation

Consider an item with the following properties:
- Main Unit: "Box"
- Sub Unit: "Pack" with `mainUnitPack = 12`
- Small Unit: "Piece" with `subUnitPack = 10`
- Price per Box: $100

If a user enters:
- Main: 2 Boxes
- Sub: 6 Packs
- Small: 5 Pieces

**Conversion:**
```
mainQty = 2.0
subQtyInMainUnit = 6 / 12 = 0.5 Boxes
smallQtyInMainUnit = (5 / 10) / 12 = 0.5 / 12 = 0.0417 Boxes

totalQty = 2.0 + 0.5 + 0.0417 = 2.5417 Boxes
totalPrice = 2.5417 × $100 = $254.17
```

## Input Validation

The quantity dialog implements several validation rules:

1. **Numeric Only**: Only numbers and decimal points are allowed
2. **No Leading Zeros**: Leading zeros are automatically removed (e.g., "007" becomes "7")
3. **Length Limit**: Maximum 6 characters per field
4. **Max Value Enforcement**: 
   - Sub unit cannot exceed `mainUnitPack - 1`
   - Small unit cannot exceed `subUnitPack - 1`
5. **Minimum Quantity**: Total quantity must be greater than 0

## Quantity Detail String

When an item is added to an invoice, a human-readable quantity detail string is generated:

```
Main Unit: 2
Sub Unit: 6
Small Unit: 5
```

This detail string is stored alongside the converted total quantity for display purposes.

## Price Calculation

The total price for an item is calculated as:

```
itemTotalPrice = totalQty × itemPrice
```

Where:
- `totalQty` is the sum of all converted quantities (in main unit)
- `itemPrice` is retrieved from the invoice controller based on the selected price level

## Real-time Calculation

The price is recalculated automatically whenever:
- Any quantity field changes
- The user types or modifies input
- A field is cleared or updated

This provides immediate feedback to the user about the total cost of their selection.

## Implementation Details

### Controllers
- `mainQtyController`: Initially set to "1" for quick entry
- `subQtyController`: Initially empty
- `smallQtyController`: Initially empty

### State Management
- Uses GetX reactive programming (`Rx` observables)
- `itemTotalPrice.obs` updates reactively on any quantity change

### User Experience Features
1. **Auto-clear on tap**: Tapping a field clears it for easy input
2. **Auto-remove leading zeros**: Improves data entry
3. **Real-time price display**: Shows calculated total immediately
4. **Centered text**: All quantity inputs are center-aligned for clarity
5. **Trailing pack indicators**: Shows pack size next to sub/small unit fields

## Error Handling

The system handles edge cases gracefully:
- Empty fields are treated as 0
- Division by zero is prevented by checking pack sizes > 0
- NaN values are converted to 0.0
- Invalid quantities trigger a snackbar error message
