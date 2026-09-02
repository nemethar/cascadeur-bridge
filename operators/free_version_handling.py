import bpy
import requests

PROMO_URL = "https://gist.githubusercontent.com/nemethar/1817218b6a1fa28e7469d4b0d976d0d0/raw/promocode.json"

CASCADEUR_AFFILIATE_URL = "https://cascadeur.com/plans?ref=aron"
DEFAULT_DISCOUNT = ("ARON15", 15)


def get_promo_code() -> tuple[str, int]:
    """
    Get the current promotional discount code and discount amount.

    The data is fetched from the remote configuration file when
    Blender has online access enabled. The default discount is returned if
    online access is disabled or the request fails.

    :return tuple[str, int]: Promotional discount code and discount amount.
    """
    if not bpy.app.online_access:
        return DEFAULT_DISCOUNT
    try:
        response = requests.get(PROMO_URL, timeout=0.75)
        response.raise_for_status()
        data = response.json()
        return (
            data.get("code", DEFAULT_DISCOUNT[0]),
            data.get("discount", DEFAULT_DISCOUNT[1]),
        )

    except (requests.RequestException, ValueError) as exc:
        print(f"Failed to get promo code: {exc}")
        return DEFAULT_DISCOUNT


class CBB_OT_license_required_popup(bpy.types.Operator):
    bl_idname = "cbb.license_required_popup"
    bl_label = "Cascadeur License Required"

    promo_code: bpy.props.StringProperty()
    discount: bpy.props.IntProperty()

    def invoke(self, context, event):
        self.promo_code, self.discount = get_promo_code()
        return context.window_manager.invoke_props_dialog(
            self,
            confirm_text="Get Cascadeur",
            cancel_default=False,
            width=420,
        )

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        col.label(
            text="An Indie or Pro subscription (or an active Trial)",
            icon="STATUS_WARNING_FILLED",
        )
        col.label(text="is required to move files from Cascadeur to Blender.")

        layout.separator()

        col = layout.column(align=True)
        col.label(text=f"Save {self.discount}% with discount code:")

        row = col.row(align=True)
        row.label(text=self.promo_code)

        copy_op = row.operator(
            "cbb.copy_discount_code",
            text="Copy",
            icon="COPYDOWN",
        )
        copy_op.code = self.promo_code

        layout.separator()

        col = layout.column(align=True)
        col.label(
            text="The button below uses an affiliate link.",
            icon="INFO",
        )

    def execute(self, context):
        if bpy.app.online_access:
            bpy.ops.wm.url_open(url=CASCADEUR_AFFILIATE_URL)
        else:
            context.window_manager.clipboard = CASCADEUR_AFFILIATE_URL
            self.report(
                {"INFO"},
                f"Online access is disabled in Preferences. The Cascadeur link was copied to your clipboard.",
            )
        return {"FINISHED"}


class CBB_OT_copy_discount_code(bpy.types.Operator):
    bl_idname = "cbb.copy_discount_code"
    bl_label = "Copy Discount Code"

    code: bpy.props.StringProperty()

    def execute(self, context):
        context.window_manager.clipboard = self.code
        self.report({"INFO"}, f"Copied discount code: {self.code}")
        return {"FINISHED"}
