class RequestType(object):
	def __init__(self):
		super(RequestType, self).__init__()
		# (↓) [-CELL SECTIONS-]
		self.ADD_CELL_SECTION = "ADD_CELL_SECTION"
		self.DELETE_CELL_SECTION = "DELETE_CELL_SECTION"
		self.RENAME_CELL_SECTION = "RENAME_CELL_SECTION"
		self.REICON_CELL_SECTION = "REICON_CELL_SECTION"
		self.SWAP_CELL_SECTIONS = "SWAP_CELL_SECTIONS"
		# (↓) [-CELLS-]
		self.ADD_CELL = "ADD_CELL"
		self.DELETE_CELL = "DELETE_CELL"
		self.RENAME_CELL = "RENAME_CELL"
		self.MOVE_CELL = "MOVE_CELL"
		# (↓) [-HINT SECTIONS-]
		self.ADD_HINT_SECTION = "ADD_HINT_SECTION"
		self.DELETE_HINT_SECTION = "DELETE_HINT_SECTION"
		self.RENAME_HINT_SECTION = "RENAME_HINT_SECTION"
		self.REICON_HINT_SECTION = "REICON_HINT_SECTION"
		self.SWAP_HINT_SECTIONS = "SWAP_HINT_SECTIONS"
		# (↓) [-HINTS-]
		self.ADD_HINT = "ADD_HINT"
		self.DELETE_HINT = "DELETE_HINT"
		self.RENAME_HINT = "RENAME_HINT"
		self.MOVE_HINT = "MOVE_HINT"
		# (↓) [-HINT-]
		self.EDIT_TAGS = "EDIT_TAGS"
		self.ADD_PAGE = "ADD_PAGE"
		self.DELETE_PAGE = "DELETE_PAGE"
		self.RENAME_PAGE = "RENAME_PAGE"
		self.SWAP_PAGES = "SWAP_PAGES"
		self.EDIT_PAGE_TEXT = "EDIT_PAGE_TEXT"
		self.ADD_IMAGE = "ADD_IMAGE"
		self.DELETE_IMAGE = "DELETE_IMAGE"